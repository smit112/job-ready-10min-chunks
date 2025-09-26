"""
Link analyzer for external resource validation and documentation.
Analyzes and validates links, extracts content, and builds knowledge base.
"""
import aiohttp
import asyncio
import requests
from typing import Dict, List, Any, Optional, Union, Set
from pathlib import Path
import logging
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin, urlunparse
from bs4 import BeautifulSoup
import hashlib
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


@dataclass
class LinkInfo:
    """Information about a link."""
    url: str
    title: str
    description: str
    status_code: int
    content_type: str
    content_length: int
    last_modified: Optional[str]
    etag: Optional[str]
    links_found: List[str]
    images_found: List[str]
    error_message: Optional[str]
    response_time: float
    is_valid: bool
    domain: str
    path: str
    hash: str
    analyzed_at: str


@dataclass
class LinkValidationResult:
    """Result of link validation."""
    url: str
    is_valid: bool
    status_code: int
    error_message: Optional[str]
    response_time: float
    last_checked: str
    retry_count: int = 0


@dataclass
class ContentExtraction:
    """Extracted content from a link."""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    links: List[str]
    images: List[str]
    headings: List[str]
    code_blocks: List[str]
    configuration_snippets: List[str]
    error_patterns: List[str]
    troubleshooting_info: List[str]
    extracted_at: str


class LinkAnalyzer:
    """Analyzes and validates links for configuration research."""
    
    def __init__(self, cache_dir: str, max_depth: int = 3, timeout: int = 30):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_depth = max_depth
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Cache for link validation results
        self.validation_cache = {}
        self.content_cache = {}
        
        # Configuration-related domains to prioritize
        self.config_domains = {
            'github.com', 'gitlab.com', 'bitbucket.org',
            'docs.microsoft.com', 'docs.aws.amazon.com', 'cloud.google.com',
            'kubernetes.io', 'docker.com', 'nginx.org',
            'apache.org', 'postgresql.org', 'mysql.com',
            'redis.io', 'elastic.co', 'mongodb.com'
        }
        
        # Error patterns to look for in content
        self.error_patterns = [
            r'ERROR:\s*(.+)',
            r'FATAL:\s*(.+)',
            r'Exception:\s*(.+)',
            r'Failed to\s+(.+)',
            r'Cannot\s+(.+)',
            r'Access denied',
            r'Permission denied',
            r'Connection refused',
            r'Timeout',
            r'Not found',
            r'Invalid configuration'
        ]
    
    def analyze_links(self, urls: List[str], extract_content: bool = True) -> List[LinkInfo]:
        """
        Analyze a list of URLs for configuration research - LOCAL ANALYSIS ONLY.
        
        Args:
            urls: List of URLs to analyze
            extract_content: Whether to extract content from the pages (disabled for local-only mode)
            
        Returns:
            List of LinkInfo objects
        """
        results = []
        
        # Local analysis only - no external HTTP requests
        for url in urls:
            try:
                result = self._analyze_single_link_local(url)
                results.append(result)
                logger.info(f"Analyzed link locally: {url}")
            except Exception as e:
                logger.error(f"Error analyzing link {url}: {str(e)}")
                # Create error result
                results.append(self._create_error_result(url, str(e)))
        
        return results
    
    def _analyze_single_link_local(self, url: str) -> LinkInfo:
        """Analyze a single link using local analysis only."""
        start_time = time.time()
        
        try:
            # Parse URL for local analysis
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            path = parsed_url.path
            
            # Create LinkInfo with local analysis only
            link_info = LinkInfo(
                url=url,
                title=f"Local Analysis: {parsed_url.path}",
                description="Content analysis disabled - external sources not allowed",
                status_code=200,  # Assume valid for local analysis
                content_type="text/html",
                content_length=0,
                last_modified=None,
                etag=None,
                links_found=[],
                images_found=[],
                error_message=None,
                response_time=time.time() - start_time,
                is_valid=True,  # Assume valid for local analysis
                domain=domain,
                path=path,
                hash="",
                analyzed_at=datetime.now().isoformat()
            )
            
            return link_info
            
        except Exception as e:
            response_time = time.time() - start_time
            parsed_url = urlparse(url)
            
            return LinkInfo(
                url=url,
                title='',
                description='',
                status_code=0,
                content_type='',
                content_length=0,
                last_modified=None,
                etag=None,
                links_found=[],
                images_found=[],
                error_message=str(e),
                response_time=response_time,
                is_valid=False,
                domain=parsed_url.netloc,
                path=parsed_url.path,
                hash='',
                analyzed_at=datetime.now().isoformat()
            )
    
    def _analyze_single_link(self, url: str, extract_content: bool) -> LinkInfo:
        """Analyze a single link."""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = self._get_cache_key(url)
            if cache_key in self.validation_cache:
                cached_result = self.validation_cache[cache_key]
                if self._is_cache_valid(cached_result):
                    return cached_result
            
            # Make request
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response_time = time.time() - start_time
            
            # Parse URL
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            path = parsed_url.path
            
            # Extract content if requested
            content_data = None
            if extract_content and response.status_code == 200:
                content_data = self._extract_content(response.text, url)
            
            # Create LinkInfo
            link_info = LinkInfo(
                url=url,
                title=content_data['title'] if content_data else '',
                description=content_data['description'] if content_data else '',
                status_code=response.status_code,
                content_type=response.headers.get('content-type', ''),
                content_length=len(response.content),
                last_modified=response.headers.get('last-modified'),
                etag=response.headers.get('etag'),
                links_found=content_data['links'] if content_data else [],
                images_found=content_data['images'] if content_data else [],
                error_message=None,
                response_time=response_time,
                is_valid=response.status_code < 400,
                domain=domain,
                path=path,
                hash=self._calculate_content_hash(response.content),
                analyzed_at=datetime.now().isoformat()
            )
            
            # Cache the result
            self.validation_cache[cache_key] = link_info
            
            return link_info
            
        except Exception as e:
            response_time = time.time() - start_time
            parsed_url = urlparse(url)
            
            return LinkInfo(
                url=url,
                title='',
                description='',
                status_code=0,
                content_type='',
                content_length=0,
                last_modified=None,
                etag=None,
                links_found=[],
                images_found=[],
                error_message=str(e),
                response_time=response_time,
                is_valid=False,
                domain=parsed_url.netloc,
                path=parsed_url.path,
                hash='',
                analyzed_at=datetime.now().isoformat()
            )
    
    def _extract_content(self, html_content: str, base_url: str) -> Dict[str, Any]:
        """Extract relevant content from HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ''
        
        # Extract description
        description = ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '').strip()
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http'):
                links.append(href)
            elif href.startswith('/'):
                links.append(urljoin(base_url, href))
        
        # Extract images
        images = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            if src.startswith('http'):
                images.append(src)
            elif src.startswith('/'):
                images.append(urljoin(base_url, src))
        
        # Extract headings
        headings = []
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            headings.append(heading.get_text().strip())
        
        # Extract code blocks
        code_blocks = []
        for code in soup.find_all(['code', 'pre']):
            code_text = code.get_text().strip()
            if code_text:
                code_blocks.append(code_text)
        
        # Extract configuration snippets
        config_snippets = self._extract_configuration_snippets(soup)
        
        # Extract error patterns
        error_patterns = self._extract_error_patterns(soup.get_text())
        
        # Extract troubleshooting information
        troubleshooting_info = self._extract_troubleshooting_info(soup)
        
        return {
            'title': title,
            'description': description,
            'links': links,
            'images': images,
            'headings': headings,
            'code_blocks': code_blocks,
            'configuration_snippets': config_snippets,
            'error_patterns': error_patterns,
            'troubleshooting_info': troubleshooting_info
        }
    
    def _extract_configuration_snippets(self, soup: BeautifulSoup) -> List[str]:
        """Extract configuration snippets from HTML."""
        snippets = []
        
        # Look for configuration-related content
        config_keywords = ['config', 'configuration', 'settings', 'yaml', 'json', 'ini', 'conf']
        
        for element in soup.find_all(['div', 'section', 'article', 'pre', 'code']):
            text = element.get_text().lower()
            if any(keyword in text for keyword in config_keywords):
                # Check if it contains configuration-like syntax
                if any(char in element.get_text() for char in ['{', '}', '=', ':', '|']):
                    snippets.append(element.get_text().strip())
        
        return snippets
    
    def _extract_error_patterns(self, text: str) -> List[str]:
        """Extract error patterns from text."""
        patterns = []
        
        for pattern in self.error_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            patterns.extend(matches)
        
        return list(set(patterns))  # Remove duplicates
    
    def _extract_troubleshooting_info(self, soup: BeautifulSoup) -> List[str]:
        """Extract troubleshooting information from HTML."""
        troubleshooting_info = []
        
        # Look for troubleshooting-related sections
        troubleshooting_keywords = ['troubleshoot', 'troubleshooting', 'debug', 'diagnose', 'fix', 'resolve']
        
        for element in soup.find_all(['div', 'section', 'article']):
            text = element.get_text().lower()
            if any(keyword in text for keyword in troubleshooting_keywords):
                # Extract the section content
                content = element.get_text().strip()
                if len(content) > 50:  # Only include substantial content
                    troubleshooting_info.append(content)
        
        return troubleshooting_info
    
    def validate_links(self, urls: List[str]) -> List[LinkValidationResult]:
        """
        Validate a list of links (check if they're accessible).
        
        Args:
            urls: List of URLs to validate
            
        Returns:
            List of LinkValidationResult objects
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {
                executor.submit(self._validate_single_link, url): url 
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error validating link {url}: {str(e)}")
                    results.append(LinkValidationResult(
                        url=url,
                        is_valid=False,
                        status_code=0,
                        error_message=str(e),
                        response_time=0.0,
                        last_checked=datetime.now().isoformat()
                    ))
        
        return results
    
    def _validate_single_link(self, url: str) -> LinkValidationResult:
        """Validate a single link."""
        start_time = time.time()
        
        try:
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            response_time = time.time() - start_time
            
            return LinkValidationResult(
                url=url,
                is_valid=response.status_code < 400,
                status_code=response.status_code,
                error_message=None,
                response_time=response_time,
                last_checked=datetime.now().isoformat()
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return LinkValidationResult(
                url=url,
                is_valid=False,
                status_code=0,
                error_message=str(e),
                response_time=response_time,
                last_checked=datetime.now().isoformat()
            )
    
    def crawl_links(self, start_urls: List[str], max_pages: int = 100) -> List[LinkInfo]:
        """
        Crawl links starting from given URLs.
        
        Args:
            start_urls: Starting URLs for crawling
            max_pages: Maximum number of pages to crawl
            
        Returns:
            List of LinkInfo objects for crawled pages
        """
        visited_urls = set()
        urls_to_visit = set(start_urls)
        results = []
        
        while urls_to_visit and len(results) < max_pages:
            current_batch = list(urls_to_visit)[:10]  # Process in batches
            urls_to_visit -= set(current_batch)
            
            # Analyze current batch
            batch_results = self.analyze_links(current_batch, extract_content=True)
            
            for result in batch_results:
                if result.is_valid and result.url not in visited_urls:
                    visited_urls.add(result.url)
                    results.append(result)
                    
                    # Add new links to visit (up to max_depth)
                    for link in result.links_found:
                        if (link not in visited_urls and 
                            link not in urls_to_visit and
                            self._should_crawl_link(link, result.url)):
                            urls_to_visit.add(link)
        
        return results
    
    def _should_crawl_link(self, link: str, parent_url: str) -> bool:
        """Determine if a link should be crawled."""
        parsed_link = urlparse(link)
        parsed_parent = urlparse(parent_url)
        
        # Don't crawl external domains unless they're configuration-related
        if parsed_link.netloc != parsed_parent.netloc:
            return parsed_link.netloc in self.config_domains
        
        # Don't crawl certain file types
        excluded_extensions = {'.pdf', '.doc', '.docx', '.zip', '.tar', '.gz', '.jpg', '.png', '.gif'}
        if any(link.lower().endswith(ext) for ext in excluded_extensions):
            return False
        
        return True
    
    def _get_cache_key(self, url: str) -> str:
        """Generate cache key for URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _is_cache_valid(self, cached_result: LinkInfo, max_age_hours: int = 24) -> bool:
        """Check if cached result is still valid."""
        analyzed_at = datetime.fromisoformat(cached_result.analyzed_at)
        return datetime.now() - analyzed_at < timedelta(hours=max_age_hours)
    
    def _calculate_content_hash(self, content: bytes) -> str:
        """Calculate hash of content."""
        return hashlib.sha256(content).hexdigest()
    
    def _create_error_result(self, url: str, error_message: str) -> LinkInfo:
        """Create error result for failed link analysis."""
        parsed_url = urlparse(url)
        return LinkInfo(
            url=url,
            title='',
            description='',
            status_code=0,
            content_type='',
            content_length=0,
            last_modified=None,
            etag=None,
            links_found=[],
            images_found=[],
            error_message=error_message,
            response_time=0.0,
            is_valid=False,
            domain=parsed_url.netloc,
            path=parsed_url.path,
            hash='',
            analyzed_at=datetime.now().isoformat()
        )
    
    def save_analysis_results(self, results: List[LinkInfo], output_file: Optional[str] = None) -> Path:
        """Save link analysis results to JSON file."""
        if output_file is None:
            output_file = self.cache_dir / f"link_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        else:
            output_file = Path(output_file)
        
        # Convert to dictionary for JSON serialization
        results_dict = [asdict(result) for result in results]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved link analysis results to: {output_file}")
        return output_file
    
    def load_analysis_results(self, json_file: Union[str, Path]) -> List[LinkInfo]:
        """Load link analysis results from JSON file."""
        json_file = Path(json_file)
        
        with open(json_file, 'r', encoding='utf-8') as f:
            results_dict = json.load(f)
        
        return [LinkInfo(**result) for result in results_dict]
    
    def search_links(self, 
                    query: str,
                    link_infos: List[LinkInfo],
                    search_fields: List[str] = None) -> List[Dict[str, Any]]:
        """
        Search through analyzed links.
        
        Args:
            query: Search query
            link_infos: List of LinkInfo objects to search
            search_fields: Fields to search in (default: title, description, domain)
            
        Returns:
            List of search results
        """
        if search_fields is None:
            search_fields = ['title', 'description', 'domain']
        
        results = []
        query_lower = query.lower()
        
        for link_info in link_infos:
            matches = []
            
            for field in search_fields:
                if hasattr(link_info, field):
                    field_value = getattr(link_info, field, '')
                    if query_lower in str(field_value).lower():
                        matches.append({
                            'field': field,
                            'value': field_value,
                            'match_position': str(field_value).lower().find(query_lower)
                        })
            
            if matches:
                results.append({
                    'link_info': link_info,
                    'matches': matches,
                    'relevance_score': len(matches)
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results
    
    def get_domain_statistics(self, link_infos: List[LinkInfo]) -> Dict[str, Any]:
        """Get statistics about domains in the analyzed links."""
        domain_stats = {}
        
        for link_info in link_infos:
            domain = link_info.domain
            if domain not in domain_stats:
                domain_stats[domain] = {
                    'count': 0,
                    'valid_count': 0,
                    'total_response_time': 0.0,
                    'status_codes': {},
                    'content_types': set()
                }
            
            stats = domain_stats[domain]
            stats['count'] += 1
            
            if link_info.is_valid:
                stats['valid_count'] += 1
            
            stats['total_response_time'] += link_info.response_time
            
            status_code = str(link_info.status_code)
            stats['status_codes'][status_code] = stats['status_codes'].get(status_code, 0) + 1
            
            if link_info.content_type:
                stats['content_types'].add(link_info.content_type)
        
        # Calculate averages and convert sets to lists
        for domain, stats in domain_stats.items():
            stats['validity_rate'] = stats['valid_count'] / stats['count'] if stats['count'] > 0 else 0
            stats['avg_response_time'] = stats['total_response_time'] / stats['count'] if stats['count'] > 0 else 0
            stats['content_types'] = list(stats['content_types'])
        
        return domain_stats