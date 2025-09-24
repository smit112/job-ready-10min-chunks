"""
Link Validator for Configuration Resource Checking
"""

import aiohttp
import asyncio
import validators
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse, urljoin
from loguru import logger
import time
from datetime import datetime
import ssl
import socket


class LinkValidator:
    """Validate links and external resources in configuration documents"""
    
    def __init__(self, max_concurrent: int = 10, default_timeout: int = 10):
        self.max_concurrent = max_concurrent
        self.default_timeout = default_timeout
        self.session = None
        
        # Common headers to avoid bot detection
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent,
            ssl=ssl.create_default_context()
        )
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=self.default_timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def validate_links(self, links: List[str], check_content: bool = False,
                           timeout: int = 10) -> Dict[str, Any]:
        """Validate a list of links and return detailed results"""
        try:
            start_time = time.time()
            
            # Initialize session if not already done
            if not self.session:
                async with self:
                    return await self._validate_links_internal(links, check_content, timeout)
            else:
                return await self._validate_links_internal(links, check_content, timeout)
                
        except Exception as e:
            logger.error(f"Error validating links: {str(e)}")
            raise
    
    async def _validate_links_internal(self, links: List[str], check_content: bool,
                                     timeout: int) -> Dict[str, Any]:
        """Internal method to validate links"""
        start_time = time.time()
        
        # Filter and prepare links
        valid_urls = []
        invalid_urls = []
        
        for link in links:
            if self._is_valid_url_format(link):
                valid_urls.append(link)
            else:
                invalid_urls.append({
                    "url": link,
                    "status": "invalid_format",
                    "error": "Invalid URL format",
                    "response_time": 0
                })
        
        logger.info(f"Validating {len(valid_urls)} valid URLs, {len(invalid_urls)} invalid formats")
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        # Validate URLs concurrently
        tasks = [
            self._validate_single_link(semaphore, url, check_content, timeout)
            for url in valid_urls
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful_validations = []
        failed_validations = []
        
        for result in results:
            if isinstance(result, Exception):
                failed_validations.append({
                    "url": "unknown",
                    "status": "error",
                    "error": str(result),
                    "response_time": 0
                })
            else:
                if result["status"] in ["success", "redirect"]:
                    successful_validations.append(result)
                else:
                    failed_validations.append(result)
        
        # Add invalid format URLs to failed validations
        failed_validations.extend(invalid_urls)
        
        # Calculate statistics
        total_time = time.time() - start_time
        total_links = len(links)
        successful_count = len(successful_validations)
        failed_count = len(failed_validations)
        
        # Generate summary
        summary = {
            "total_links": total_links,
            "successful": successful_count,
            "failed": failed_count,
            "success_rate": (successful_count / total_links * 100) if total_links > 0 else 0,
            "total_validation_time": round(total_time, 2),
            "average_response_time": self._calculate_average_response_time(successful_validations),
            "validation_timestamp": datetime.now().isoformat()
        }
        
        # Categorize failures
        failure_analysis = self._analyze_failures(failed_validations)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(summary, failure_analysis)
        
        return {
            "summary": summary,
            "successful_validations": successful_validations,
            "failed_validations": failed_validations,
            "failure_analysis": failure_analysis,
            "recommendations": recommendations
        }
    
    async def _validate_single_link(self, semaphore: asyncio.Semaphore, url: str,
                                  check_content: bool, timeout: int) -> Dict[str, Any]:
        """Validate a single link"""
        async with semaphore:
            start_time = time.time()
            
            try:
                # Set custom timeout for this request
                custom_timeout = aiohttp.ClientTimeout(total=timeout)
                
                async with self.session.get(url, timeout=custom_timeout, allow_redirects=True) as response:
                    response_time = round((time.time() - start_time) * 1000, 2)  # in milliseconds
                    
                    result = {
                        "url": url,
                        "status_code": response.status,
                        "response_time": response_time,
                        "final_url": str(response.url),
                        "redirected": str(response.url) != url,
                        "content_type": response.headers.get('Content-Type', 'unknown'),
                        "content_length": response.headers.get('Content-Length', 'unknown'),
                        "server": response.headers.get('Server', 'unknown')
                    }
                    
                    # Determine status based on HTTP status code
                    if 200 <= response.status < 300:
                        result["status"] = "success"
                    elif 300 <= response.status < 400:
                        result["status"] = "redirect"
                    elif 400 <= response.status < 500:
                        result["status"] = "client_error"
                        result["error"] = f"HTTP {response.status}: Client Error"
                    elif 500 <= response.status < 600:
                        result["status"] = "server_error"
                        result["error"] = f"HTTP {response.status}: Server Error"
                    else:
                        result["status"] = "unknown_status"
                        result["error"] = f"HTTP {response.status}: Unknown Status"
                    
                    # Check content if requested and successful
                    if check_content and result["status"] == "success":
                        content_analysis = await self._analyze_content(response)
                        result["content_analysis"] = content_analysis
                    
                    return result
                    
            except asyncio.TimeoutError:
                return {
                    "url": url,
                    "status": "timeout",
                    "error": f"Request timed out after {timeout} seconds",
                    "response_time": timeout * 1000
                }
            except aiohttp.ClientError as e:
                return {
                    "url": url,
                    "status": "connection_error",
                    "error": f"Connection error: {str(e)}",
                    "response_time": round((time.time() - start_time) * 1000, 2)
                }
            except Exception as e:
                return {
                    "url": url,
                    "status": "error",
                    "error": f"Unexpected error: {str(e)}",
                    "response_time": round((time.time() - start_time) * 1000, 2)
                }
    
    async def _analyze_content(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Analyze content of successful responses"""
        try:
            content_analysis = {
                "has_content": False,
                "content_size": 0,
                "content_preview": "",
                "is_html": False,
                "is_json": False,
                "is_xml": False
            }
            
            content_type = response.headers.get('Content-Type', '').lower()
            
            # Read a portion of content for analysis
            content_chunk = await response.content.read(1024)  # Read first 1KB
            content_analysis["content_size"] = len(content_chunk)
            content_analysis["has_content"] = len(content_chunk) > 0
            
            if content_chunk:
                try:
                    content_text = content_chunk.decode('utf-8', errors='ignore')
                    content_analysis["content_preview"] = content_text[:200] + "..." if len(content_text) > 200 else content_text
                    
                    # Detect content types
                    content_analysis["is_html"] = 'html' in content_type or '<html' in content_text.lower()
                    content_analysis["is_json"] = 'json' in content_type or content_text.strip().startswith(('{', '['))
                    content_analysis["is_xml"] = 'xml' in content_type or content_text.strip().startswith('<?xml')
                    
                except UnicodeDecodeError:
                    content_analysis["content_preview"] = "Binary content - cannot preview"
            
            return content_analysis
            
        except Exception as e:
            logger.warning(f"Error analyzing content: {str(e)}")
            return {"error": f"Content analysis failed: {str(e)}"}
    
    def _is_valid_url_format(self, url: str) -> bool:
        """Check if URL has valid format"""
        try:
            # Use validators library for basic validation
            if not validators.url(url):
                return False
            
            # Additional checks
            parsed = urlparse(url)
            
            # Must have scheme and netloc
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Must be http or https
            if parsed.scheme.lower() not in ['http', 'https']:
                return False
            
            return True
            
        except Exception:
            return False
    
    def _calculate_average_response_time(self, successful_validations: List[Dict[str, Any]]) -> float:
        """Calculate average response time for successful validations"""
        if not successful_validations:
            return 0.0
        
        total_time = sum(result.get("response_time", 0) for result in successful_validations)
        return round(total_time / len(successful_validations), 2)
    
    def _analyze_failures(self, failed_validations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze failure patterns in failed validations"""
        failure_analysis = {
            "failure_categories": {},
            "common_errors": {},
            "timeout_count": 0,
            "connection_error_count": 0,
            "client_error_count": 0,
            "server_error_count": 0
        }
        
        try:
            for failure in failed_validations:
                status = failure.get("status", "unknown")
                error = failure.get("error", "")
                
                # Count by status
                if status not in failure_analysis["failure_categories"]:
                    failure_analysis["failure_categories"][status] = 0
                failure_analysis["failure_categories"][status] += 1
                
                # Count specific error types
                if status == "timeout":
                    failure_analysis["timeout_count"] += 1
                elif status == "connection_error":
                    failure_analysis["connection_error_count"] += 1
                elif status == "client_error":
                    failure_analysis["client_error_count"] += 1
                elif status == "server_error":
                    failure_analysis["server_error_count"] += 1
                
                # Track common error messages
                if error:
                    if error not in failure_analysis["common_errors"]:
                        failure_analysis["common_errors"][error] = 0
                    failure_analysis["common_errors"][error] += 1
            
            return failure_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing failures: {str(e)}")
            return failure_analysis
    
    def _generate_recommendations(self, summary: Dict[str, Any], 
                                failure_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        try:
            success_rate = summary.get("success_rate", 0)
            timeout_count = failure_analysis.get("timeout_count", 0)
            connection_error_count = failure_analysis.get("connection_error_count", 0)
            client_error_count = failure_analysis.get("client_error_count", 0)
            server_error_count = failure_analysis.get("server_error_count", 0)
            
            # Success rate recommendations
            if success_rate < 50:
                recommendations.append("CRITICAL: Less than 50% of links are accessible. Review and update configuration immediately.")
            elif success_rate < 80:
                recommendations.append("WARNING: Success rate below 80%. Consider reviewing failed links.")
            elif success_rate >= 95:
                recommendations.append("EXCELLENT: High success rate. Configuration links are well maintained.")
            
            # Specific issue recommendations
            if timeout_count > 0:
                recommendations.append(f"Consider increasing timeout values - {timeout_count} links timed out.")
            
            if connection_error_count > 0:
                recommendations.append(f"Check network connectivity and firewall settings - {connection_error_count} connection errors.")
            
            if client_error_count > 0:
                recommendations.append(f"Review and update URLs - {client_error_count} client errors (404, etc.).")
            
            if server_error_count > 0:
                recommendations.append(f"Contact service providers - {server_error_count} server errors detected.")
            
            # Performance recommendations
            avg_response_time = summary.get("average_response_time", 0)
            if avg_response_time > 5000:  # 5 seconds
                recommendations.append("Consider optimizing slow-responding services or implementing caching.")
            
            # General recommendations
            if summary.get("total_links", 0) > 0:
                recommendations.extend([
                    "Implement regular automated link checking",
                    "Set up monitoring alerts for critical service URLs",
                    "Document backup URLs for critical services",
                    "Consider implementing health check endpoints"
                ])
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return ["Error generating recommendations - manual review required"]