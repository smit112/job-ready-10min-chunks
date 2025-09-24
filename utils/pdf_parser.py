"""
PDF parser for error documentation and troubleshooting guides.
Extracts and processes information from PDF files for configuration research.
"""
import PyPDF2
import fitz  # PyMuPDF
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import logging
import re
import json
from dataclasses import dataclass
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class PDFDocument:
    """Represents a parsed PDF document."""
    file_path: str
    title: str
    content: str
    pages: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    error_patterns: List[Dict[str, Any]]
    troubleshooting_steps: List[Dict[str, Any]]
    configuration_snippets: List[Dict[str, Any]]
    hash: str


@dataclass
class ErrorPattern:
    """Represents an error pattern found in PDF."""
    pattern: str
    description: str
    severity: str
    solution: str
    page_number: int
    context: str


@dataclass
class TroubleshootingStep:
    """Represents a troubleshooting step from PDF."""
    step_number: int
    description: str
    commands: List[str]
    expected_output: str
    page_number: int
    category: str


class PDFParser:
    """Parses PDF files for configuration research and troubleshooting."""
    
    def __init__(self, docs_dir: str, errors_dir: str):
        self.docs_dir = Path(docs_dir)
        self.errors_dir = Path(errors_dir)
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.errors_dir.mkdir(parents=True, exist_ok=True)
        
        # Common error patterns to look for
        self.error_patterns = [
            r'ERROR:\s*(.+)',
            r'FATAL:\s*(.+)',
            r'CRITICAL:\s*(.+)',
            r'Exception:\s*(.+)',
            r'Failed to\s+(.+)',
            r'Cannot\s+(.+)',
            r'Unable to\s+(.+)',
            r'Access denied',
            r'Permission denied',
            r'Connection refused',
            r'Timeout',
            r'Not found',
            r'Invalid configuration',
            r'Missing required',
        ]
        
        # Troubleshooting keywords
        self.troubleshooting_keywords = [
            'troubleshoot', 'troubleshooting', 'debug', 'diagnose',
            'fix', 'resolve', 'solution', 'workaround', 'step',
            'check', 'verify', 'validate', 'test'
        ]
    
    def parse_pdf(self, file_path: Union[str, Path]) -> PDFDocument:
        """
        Parse a PDF file and extract relevant information.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            PDFDocument object with extracted information
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        try:
            # Use PyMuPDF for better text extraction
            doc = fitz.open(file_path)
            
            # Extract metadata
            metadata = doc.metadata
            title = metadata.get('title', file_path.stem)
            
            # Extract content and pages
            pages = []
            full_content = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                full_content += text + "\n"
                
                pages.append({
                    'page_number': page_num + 1,
                    'content': text,
                    'char_count': len(text),
                    'word_count': len(text.split())
                })
            
            doc.close()
            
            # Calculate file hash
            file_hash = self._calculate_file_hash(file_path)
            
            # Extract error patterns
            error_patterns = self._extract_error_patterns(full_content, pages)
            
            # Extract troubleshooting steps
            troubleshooting_steps = self._extract_troubleshooting_steps(full_content, pages)
            
            # Extract configuration snippets
            config_snippets = self._extract_configuration_snippets(full_content, pages)
            
            pdf_doc = PDFDocument(
                file_path=str(file_path),
                title=title,
                content=full_content,
                pages=pages,
                metadata=metadata,
                error_patterns=error_patterns,
                troubleshooting_steps=troubleshooting_steps,
                configuration_snippets=config_snippets,
                hash=file_hash
            )
            
            logger.info(f"Successfully parsed PDF: {file_path}")
            return pdf_doc
            
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {str(e)}")
            raise
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of the file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _extract_error_patterns(self, content: str, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract error patterns from PDF content."""
        error_patterns = []
        
        for pattern in self.error_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                # Find which page this match is on
                page_number = self._find_page_for_position(match.start(), pages)
                
                # Extract context around the match
                context_start = max(0, match.start() - 100)
                context_end = min(len(content), match.end() + 100)
                context = content[context_start:context_end].strip()
                
                # Determine severity
                severity = self._determine_error_severity(match.group(0))
                
                error_patterns.append({
                    'pattern': match.group(0),
                    'description': match.group(1) if match.groups() else match.group(0),
                    'severity': severity,
                    'solution': self._extract_solution_nearby(content, match.start()),
                    'page_number': page_number,
                    'context': context
                })
        
        return error_patterns
    
    def _extract_troubleshooting_steps(self, content: str, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract troubleshooting steps from PDF content."""
        steps = []
        
        # Look for numbered steps
        step_pattern = r'(?:Step\s+(\d+)|(\d+)\.)\s*([^\n]+(?:\n(?!\d+\.)[^\n]*)*)'
        matches = re.finditer(step_pattern, content, re.IGNORECASE | re.MULTILINE)
        
        for match in matches:
            step_number = int(match.group(1) or match.group(2))
            description = match.group(3).strip()
            
            # Find which page this step is on
            page_number = self._find_page_for_position(match.start(), pages)
            
            # Extract commands from the step
            commands = self._extract_commands_from_text(description)
            
            # Determine category
            category = self._categorize_troubleshooting_step(description)
            
            steps.append({
                'step_number': step_number,
                'description': description,
                'commands': commands,
                'expected_output': self._extract_expected_output(content, match.start()),
                'page_number': page_number,
                'category': category
            })
        
        return steps
    
    def _extract_configuration_snippets(self, content: str, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract configuration code snippets from PDF content."""
        snippets = []
        
        # Look for code blocks, configuration sections
        code_patterns = [
            r'```([^`]+)```',  # Markdown code blocks
            r'<code>([^<]+)</code>',  # HTML code tags
            r'Configuration:\s*\n([^\n]+(?:\n[^\n]+)*)',  # Configuration sections
            r'Example:\s*\n([^\n]+(?:\n[^\n]+)*)',  # Example sections
        ]
        
        for pattern in code_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                snippet_content = match.group(1).strip()
                
                # Find which page this snippet is on
                page_number = self._find_page_for_position(match.start(), pages)
                
                # Determine snippet type
                snippet_type = self._determine_snippet_type(snippet_content)
                
                snippets.append({
                    'content': snippet_content,
                    'type': snippet_type,
                    'page_number': page_number,
                    'language': self._detect_language(snippet_content)
                })
        
        return snippets
    
    def _find_page_for_position(self, position: int, pages: List[Dict[str, Any]]) -> int:
        """Find which page a character position belongs to."""
        current_pos = 0
        for page in pages:
            current_pos += len(page['content']) + 1  # +1 for newline
            if position < current_pos:
                return page['page_number']
        return len(pages)
    
    def _determine_error_severity(self, error_text: str) -> str:
        """Determine error severity based on keywords."""
        error_lower = error_text.lower()
        
        if any(word in error_lower for word in ['fatal', 'critical', 'emergency']):
            return 'CRITICAL'
        elif any(word in error_lower for word in ['error', 'failed', 'cannot']):
            return 'ERROR'
        elif any(word in error_lower for word in ['warning', 'warn']):
            return 'WARNING'
        else:
            return 'INFO'
    
    def _extract_solution_nearby(self, content: str, position: int) -> str:
        """Extract solution text near an error."""
        # Look for solution keywords in the surrounding text
        context_start = max(0, position - 500)
        context_end = min(len(content), position + 500)
        context = content[context_start:context_end]
        
        solution_patterns = [
            r'Solution:\s*([^\n]+(?:\n[^\n]+)*)',
            r'Fix:\s*([^\n]+(?:\n[^\n]+)*)',
            r'Resolution:\s*([^\n]+(?:\n[^\n]+)*)',
            r'To resolve:\s*([^\n]+(?:\n[^\n]+)*)',
        ]
        
        for pattern in solution_patterns:
            match = re.search(pattern, context, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_commands_from_text(self, text: str) -> List[str]:
        """Extract command-line commands from text."""
        # Look for commands (lines starting with $, >, or common command patterns)
        command_patterns = [
            r'\$\s*([^\n]+)',
            r'>\s*([^\n]+)',
            r'(?:sudo\s+)?[a-zA-Z][a-zA-Z0-9_-]+\s+[^\n]+',
        ]
        
        commands = []
        for pattern in command_patterns:
            matches = re.findall(pattern, text)
            commands.extend(matches)
        
        return commands
    
    def _categorize_troubleshooting_step(self, description: str) -> str:
        """Categorize troubleshooting step based on content."""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ['check', 'verify', 'validate']):
            return 'VERIFICATION'
        elif any(word in desc_lower for word in ['install', 'update', 'upgrade']):
            return 'INSTALLATION'
        elif any(word in desc_lower for word in ['configure', 'setting', 'config']):
            return 'CONFIGURATION'
        elif any(word in desc_lower for word in ['restart', 'reboot', 'reload']):
            return 'RESTART'
        elif any(word in desc_lower for word in ['log', 'debug', 'trace']):
            return 'DEBUGGING'
        else:
            return 'GENERAL'
    
    def _extract_expected_output(self, content: str, position: int) -> str:
        """Extract expected output near a troubleshooting step."""
        context_start = max(0, position - 300)
        context_end = min(len(content), position + 300)
        context = content[context_start:context_end]
        
        output_patterns = [
            r'Expected output:\s*([^\n]+(?:\n[^\n]+)*)',
            r'You should see:\s*([^\n]+(?:\n[^\n]+)*)',
            r'Output:\s*([^\n]+(?:\n[^\n]+)*)',
        ]
        
        for pattern in output_patterns:
            match = re.search(pattern, context, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _determine_snippet_type(self, content: str) -> str:
        """Determine the type of configuration snippet."""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['config', 'configuration', 'settings']):
            return 'CONFIGURATION'
        elif any(word in content_lower for word in ['example', 'sample']):
            return 'EXAMPLE'
        elif any(word in content_lower for word in ['script', 'command']):
            return 'SCRIPT'
        else:
            return 'CODE'
    
    def _detect_language(self, content: str) -> str:
        """Detect programming/configuration language."""
        # Simple language detection based on keywords and syntax
        if '#!/bin/bash' in content or 'echo' in content:
            return 'bash'
        elif 'python' in content or 'import' in content:
            return 'python'
        elif '{' in content and '}' in content and ':' in content:
            return 'json'
        elif 'server {' in content or 'location {' in content:
            return 'nginx'
        elif 'Host' in content and 'User' in content:
            return 'ssh'
        else:
            return 'text'
    
    def save_parsed_document(self, pdf_doc: PDFDocument, output_file: Optional[str] = None) -> Path:
        """Save parsed PDF document to JSON file."""
        if output_file is None:
            output_file = self.docs_dir / f"{Path(pdf_doc.file_path).stem}_parsed.json"
        else:
            output_file = Path(output_file)
        
        # Convert to dictionary for JSON serialization
        doc_dict = {
            'file_path': pdf_doc.file_path,
            'title': pdf_doc.title,
            'content': pdf_doc.content,
            'pages': pdf_doc.pages,
            'metadata': pdf_doc.metadata,
            'error_patterns': pdf_doc.error_patterns,
            'troubleshooting_steps': pdf_doc.troubleshooting_steps,
            'configuration_snippets': pdf_doc.configuration_snippets,
            'hash': pdf_doc.hash,
            'parsed_at': datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(doc_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved parsed document to: {output_file}")
        return output_file
    
    def load_parsed_document(self, json_file: Union[str, Path]) -> PDFDocument:
        """Load a previously parsed PDF document from JSON file."""
        json_file = Path(json_file)
        
        with open(json_file, 'r', encoding='utf-8') as f:
            doc_dict = json.load(f)
        
        return PDFDocument(
            file_path=doc_dict['file_path'],
            title=doc_dict['title'],
            content=doc_dict['content'],
            pages=doc_dict['pages'],
            metadata=doc_dict['metadata'],
            error_patterns=doc_dict['error_patterns'],
            troubleshooting_steps=doc_dict['troubleshooting_steps'],
            configuration_snippets=doc_dict['configuration_snippets'],
            hash=doc_dict['hash']
        )
    
    def search_documents(self, 
                        query: str,
                        parsed_docs: List[PDFDocument],
                        search_type: str = 'all') -> List[Dict[str, Any]]:
        """
        Search through parsed PDF documents.
        
        Args:
            query: Search query
            parsed_docs: List of parsed PDF documents
            search_type: Type of search ('all', 'errors', 'troubleshooting', 'config')
            
        Returns:
            List of search results
        """
        results = []
        query_lower = query.lower()
        
        for doc in parsed_docs:
            doc_results = {
                'document': doc.title,
                'file_path': doc.file_path,
                'matches': []
            }
            
            if search_type in ['all', 'errors']:
                # Search error patterns
                for error in doc.error_patterns:
                    if (query_lower in error['pattern'].lower() or 
                        query_lower in error['description'].lower()):
                        doc_results['matches'].append({
                            'type': 'error',
                            'content': error,
                            'page': error['page_number']
                        })
            
            if search_type in ['all', 'troubleshooting']:
                # Search troubleshooting steps
                for step in doc.troubleshooting_steps:
                    if query_lower in step['description'].lower():
                        doc_results['matches'].append({
                            'type': 'troubleshooting',
                            'content': step,
                            'page': step['page_number']
                        })
            
            if search_type in ['all', 'config']:
                # Search configuration snippets
                for snippet in doc.configuration_snippets:
                    if query_lower in snippet['content'].lower():
                        doc_results['matches'].append({
                            'type': 'configuration',
                            'content': snippet,
                            'page': snippet['page_number']
                        })
            
            if doc_results['matches']:
                results.append(doc_results)
        
        return results