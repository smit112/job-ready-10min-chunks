"""
AI-powered troubleshooting assistant with knowledge base integration.
Provides intelligent troubleshooting recommendations based on configuration analysis.
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import json
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid
import re
from collections import defaultdict

# AI/ML imports
try:
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.chains import RetrievalQA
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    logging.warning("AI libraries not available. Some features will be disabled.")

from configs.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class TroubleshootingCase:
    """Represents a troubleshooting case."""
    case_id: str
    title: str
    description: str
    error_messages: List[str]
    configuration_context: Dict[str, Any]
    environment_info: Dict[str, Any]
    severity: str  # 'critical', 'high', 'medium', 'low'
    status: str  # 'open', 'investigating', 'resolved', 'closed'
    created_at: str
    updated_at: str
    resolution: Optional[str] = None
    tags: List[str] = None


@dataclass
class TroubleshootingRecommendation:
    """Represents a troubleshooting recommendation."""
    recommendation_id: str
    case_id: str
    title: str
    description: str
    steps: List[Dict[str, Any]]
    confidence_score: float
    reasoning: str
    source: str  # 'ai', 'knowledge_base', 'pattern_match'
    created_at: str
    category: str  # 'diagnosis', 'fix', 'prevention', 'monitoring'


@dataclass
class KnowledgeBaseEntry:
    """Represents a knowledge base entry."""
    entry_id: str
    title: str
    content: str
    category: str
    tags: List[str]
    error_patterns: List[str]
    solutions: List[str]
    configuration_examples: List[Dict[str, Any]]
    created_at: str
    updated_at: str
    usage_count: int = 0
    success_rate: float = 0.0


class TroubleshootingAI:
    """AI-powered troubleshooting assistant with knowledge base integration."""
    
    def __init__(self):
        self.knowledge_base: Dict[str, KnowledgeBaseEntry] = {}
        self.troubleshooting_cases: Dict[str, TroubleshootingCase] = {}
        self.recommendations: Dict[str, TroubleshootingRecommendation] = {}
        
        # AI components
        self.llm = None
        self.embeddings = None
        self.vector_store = None
        self.sentence_model = None
        self.tfidf_vectorizer = None
        
        # Pattern matching
        self.error_patterns = defaultdict(list)
        self.solution_patterns = defaultdict(list)
        
        # Initialize AI components if available
        if AI_AVAILABLE:
            self._initialize_ai_components()
        
        # Load default knowledge base
        self._load_default_knowledge_base()
        
        logger.info("Troubleshooting AI initialized")
    
    def _initialize_ai_components(self):
        """Initialize AI components."""
        try:
            if settings.openai_api_key:
                self.llm = ChatOpenAI(
                    model_name=settings.default_model,
                    temperature=settings.temperature,
                    max_tokens=settings.max_tokens,
                    openai_api_key=settings.openai_api_key
                )
                self.embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
                logger.info("OpenAI components initialized")
            
            # Initialize sentence transformer for local embeddings
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize TF-IDF vectorizer
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            logger.info("AI components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI components: {str(e)}")
            self.llm = None
            self.embeddings = None
    
    def _load_default_knowledge_base(self):
        """Load default knowledge base entries."""
        default_entries = [
            KnowledgeBaseEntry(
                entry_id="kb_001",
                title="Database Connection Issues",
                content="Common database connection problems and solutions",
                category="database",
                tags=["connection", "database", "timeout", "authentication"],
                error_patterns=[
                    "Connection refused",
                    "Authentication failed",
                    "Connection timeout",
                    "Database not found"
                ],
                solutions=[
                    "Check database server status",
                    "Verify connection parameters",
                    "Check network connectivity",
                    "Validate credentials"
                ],
                configuration_examples=[
                    {
                        "type": "connection_string",
                        "example": "postgresql://user:password@host:port/database",
                        "description": "Standard PostgreSQL connection string"
                    }
                ],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            ),
            KnowledgeBaseEntry(
                entry_id="kb_002",
                title="API Configuration Errors",
                content="Common API configuration issues and troubleshooting steps",
                category="api",
                tags=["api", "configuration", "endpoint", "authentication"],
                error_patterns=[
                    "Invalid endpoint",
                    "Authentication failed",
                    "Rate limit exceeded",
                    "Invalid API key"
                ],
                solutions=[
                    "Verify API endpoint URL",
                    "Check API key validity",
                    "Review rate limiting settings",
                    "Validate request format"
                ],
                configuration_examples=[
                    {
                        "type": "api_config",
                        "example": {
                            "base_url": "https://api.example.com",
                            "api_key": "your-api-key",
                            "timeout": 30
                        },
                        "description": "Standard API configuration"
                    }
                ],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            ),
            KnowledgeBaseEntry(
                entry_id="kb_003",
                title="File Permission Issues",
                content="Common file permission problems and solutions",
                category="filesystem",
                tags=["permissions", "file", "access", "security"],
                error_patterns=[
                    "Permission denied",
                    "Access denied",
                    "File not found",
                    "Read-only file system"
                ],
                solutions=[
                    "Check file permissions",
                    "Verify user ownership",
                    "Check disk space",
                    "Review SELinux/AppArmor settings"
                ],
                configuration_examples=[
                    {
                        "type": "file_permissions",
                        "example": "chmod 644 /path/to/file",
                        "description": "Set read permissions for owner and group"
                    }
                ],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
        ]
        
        for entry in default_entries:
            self.knowledge_base[entry.entry_id] = entry
        
        logger.info(f"Loaded {len(default_entries)} default knowledge base entries")
    
    def create_troubleshooting_case(self,
                                  title: str,
                                  description: str,
                                  error_messages: List[str],
                                  configuration_context: Dict[str, Any],
                                  environment_info: Dict[str, Any],
                                  severity: str = "medium") -> str:
        """
        Create a new troubleshooting case.
        
        Args:
            title: Case title
            description: Case description
            error_messages: List of error messages
            configuration_context: Configuration context
            environment_info: Environment information
            severity: Case severity
            
        Returns:
            Case ID
        """
        case_id = str(uuid.uuid4())
        
        case = TroubleshootingCase(
            case_id=case_id,
            title=title,
            description=description,
            error_messages=error_messages,
            configuration_context=configuration_context,
            environment_info=environment_info,
            severity=severity,
            status="open",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            tags=[]
        )
        
        self.troubleshooting_cases[case_id] = case
        
        # Index error patterns
        for error in error_messages:
            self.error_patterns[error.lower()].append(case_id)
        
        logger.info(f"Created troubleshooting case: {case_id}")
        return case_id
    
    async def generate_recommendations(self, case_id: str) -> List[TroubleshootingRecommendation]:
        """
        Generate troubleshooting recommendations for a case.
        
        Args:
            case_id: ID of the troubleshooting case
            
        Returns:
            List of troubleshooting recommendations
        """
        if case_id not in self.troubleshooting_cases:
            raise ValueError(f"Case {case_id} not found")
        
        case = self.troubleshooting_cases[case_id]
        recommendations = []
        
        # Generate recommendations using different methods
        kb_recommendations = await self._generate_kb_recommendations(case)
        pattern_recommendations = await self._generate_pattern_recommendations(case)
        
        if AI_AVAILABLE and self.llm:
            ai_recommendations = await self._generate_ai_recommendations(case)
            recommendations.extend(ai_recommendations)
        
        recommendations.extend(kb_recommendations)
        recommendations.extend(pattern_recommendations)
        
        # Store recommendations
        for rec in recommendations:
            self.recommendations[rec.recommendation_id] = rec
        
        logger.info(f"Generated {len(recommendations)} recommendations for case {case_id}")
        return recommendations
    
    async def _generate_kb_recommendations(self, case: TroubleshootingCase) -> List[TroubleshootingRecommendation]:
        """Generate recommendations from knowledge base."""
        recommendations = []
        
        # Find relevant knowledge base entries
        relevant_entries = self._find_relevant_kb_entries(case)
        
        for entry in relevant_entries:
            # Calculate confidence based on pattern matching
            confidence = self._calculate_pattern_confidence(case.error_messages, entry.error_patterns)
            
            if confidence > 0.3:  # Threshold for relevance
                recommendation = TroubleshootingRecommendation(
                    recommendation_id=str(uuid.uuid4()),
                    case_id=case.case_id,
                    title=f"KB: {entry.title}",
                    description=entry.content,
                    steps=self._convert_solutions_to_steps(entry.solutions),
                    confidence_score=confidence,
                    reasoning=f"Based on knowledge base entry {entry.entry_id} with {confidence:.2f} confidence",
                    source="knowledge_base",
                    created_at=datetime.now().isoformat(),
                    category="diagnosis"
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    async def _generate_pattern_recommendations(self, case: TroubleshootingCase) -> List[TroubleshootingRecommendation]:
        """Generate recommendations based on pattern matching."""
        recommendations = []
        
        # Find similar cases
        similar_cases = self._find_similar_cases(case)
        
        for similar_case_id, similarity_score in similar_cases:
            if similarity_score > 0.5:
                similar_case = self.troubleshooting_cases[similar_case_id]
                
                # Check if similar case has resolution
                if similar_case.resolution:
                    recommendation = TroubleshootingRecommendation(
                        recommendation_id=str(uuid.uuid4()),
                        case_id=case.case_id,
                        title=f"Similar Case Resolution: {similar_case.title}",
                        description=f"Based on similar case {similar_case_id}",
                        steps=[{"step": 1, "description": similar_case.resolution}],
                        confidence_score=similarity_score,
                        reasoning=f"Pattern match with case {similar_case_id} (similarity: {similarity_score:.2f})",
                        source="pattern_match",
                        created_at=datetime.now().isoformat(),
                        category="fix"
                    )
                    recommendations.append(recommendation)
        
        return recommendations
    
    async def _generate_ai_recommendations(self, case: TroubleshootingCase) -> List[TroubleshootingRecommendation]:
        """Generate recommendations using AI."""
        recommendations = []
        
        try:
            # Prepare context for AI
            context = self._prepare_ai_context(case)
            
            # Generate AI response
            messages = [
                SystemMessage(content="You are a configuration troubleshooting expert. Provide specific, actionable recommendations."),
                HumanMessage(content=context)
            ]
            
            response = await self.llm.agenerate([messages])
            ai_response = response.generations[0][0].text
            
            # Parse AI response
            parsed_recommendations = self._parse_ai_response(ai_response, case.case_id)
            recommendations.extend(parsed_recommendations)
            
        except Exception as e:
            logger.error(f"Error generating AI recommendations: {str(e)}")
        
        return recommendations
    
    def _find_relevant_kb_entries(self, case: TroubleshootingCase) -> List[KnowledgeBaseEntry]:
        """Find relevant knowledge base entries for a case."""
        relevant_entries = []
        
        for entry in self.knowledge_base.values():
            # Check tag matching
            case_tags = set(case.tags or [])
            entry_tags = set(entry.tags)
            tag_overlap = len(case_tags.intersection(entry_tags))
            
            # Check error pattern matching
            pattern_matches = 0
            for error in case.error_messages:
                for pattern in entry.error_patterns:
                    if pattern.lower() in error.lower():
                        pattern_matches += 1
            
            # Calculate relevance score
            relevance_score = tag_overlap + pattern_matches
            
            if relevance_score > 0:
                relevant_entries.append((entry, relevance_score))
        
        # Sort by relevance and return top entries
        relevant_entries.sort(key=lambda x: x[1], reverse=True)
        return [entry for entry, score in relevant_entries[:5]]
    
    def _calculate_pattern_confidence(self, error_messages: List[str], patterns: List[str]) -> float:
        """Calculate confidence score based on pattern matching."""
        if not error_messages or not patterns:
            return 0.0
        
        matches = 0
        total_patterns = len(patterns)
        
        for error in error_messages:
            error_lower = error.lower()
            for pattern in patterns:
                if pattern.lower() in error_lower:
                    matches += 1
        
        return matches / total_patterns if total_patterns > 0 else 0.0
    
    def _convert_solutions_to_steps(self, solutions: List[str]) -> List[Dict[str, Any]]:
        """Convert solution strings to structured steps."""
        steps = []
        for i, solution in enumerate(solutions, 1):
            steps.append({
                "step": i,
                "description": solution,
                "status": "pending"
            })
        return steps
    
    def _find_similar_cases(self, case: TroubleshootingCase) -> List[tuple]:
        """Find similar cases based on error patterns and context."""
        similar_cases = []
        
        for case_id, other_case in self.troubleshooting_cases.items():
            if case_id == case.case_id:
                continue
            
            # Calculate similarity based on error messages
            similarity = self._calculate_case_similarity(case, other_case)
            
            if similarity > 0.3:
                similar_cases.append((case_id, similarity))
        
        # Sort by similarity
        similar_cases.sort(key=lambda x: x[1], reverse=True)
        return similar_cases[:3]
    
    def _calculate_case_similarity(self, case1: TroubleshootingCase, case2: TroubleshootingCase) -> float:
        """Calculate similarity between two cases."""
        # Simple similarity based on error message overlap
        errors1 = set(error.lower() for error in case1.error_messages)
        errors2 = set(error.lower() for error in case2.error_messages)
        
        if not errors1 or not errors2:
            return 0.0
        
        intersection = len(errors1.intersection(errors2))
        union = len(errors1.union(errors2))
        
        return intersection / union if union > 0 else 0.0
    
    def _prepare_ai_context(self, case: TroubleshootingCase) -> str:
        """Prepare context for AI analysis."""
        context = f"""
Troubleshooting Case Analysis:

Title: {case.title}
Description: {case.description}
Severity: {case.severity}

Error Messages:
{chr(10).join(f"- {error}" for error in case.error_messages)}

Configuration Context:
{json.dumps(case.configuration_context, indent=2)}

Environment Info:
{json.dumps(case.environment_info, indent=2)}

Please provide specific, actionable troubleshooting recommendations with steps.
"""
        return context
    
    def _parse_ai_response(self, ai_response: str, case_id: str) -> List[TroubleshootingRecommendation]:
        """Parse AI response into structured recommendations."""
        recommendations = []
        
        # Simple parsing - can be enhanced
        lines = ai_response.split('\n')
        current_recommendation = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a new recommendation
            if line.startswith('Recommendation') or line.startswith('Solution'):
                if current_recommendation:
                    recommendations.append(current_recommendation)
                
                current_recommendation = TroubleshootingRecommendation(
                    recommendation_id=str(uuid.uuid4()),
                    case_id=case_id,
                    title=line,
                    description="",
                    steps=[],
                    confidence_score=0.7,  # Default confidence for AI recommendations
                    reasoning="Generated by AI analysis",
                    source="ai",
                    created_at=datetime.now().isoformat(),
                    category="diagnosis"
                )
            elif current_recommendation and line.startswith('-'):
                # This is a step
                step_num = len(current_recommendation.steps) + 1
                current_recommendation.steps.append({
                    "step": step_num,
                    "description": line[1:].strip(),
                    "status": "pending"
                })
            elif current_recommendation:
                # This is description text
                if current_recommendation.description:
                    current_recommendation.description += " " + line
                else:
                    current_recommendation.description = line
        
        # Add the last recommendation
        if current_recommendation:
            recommendations.append(current_recommendation)
        
        return recommendations
    
    def add_knowledge_base_entry(self, entry: KnowledgeBaseEntry):
        """Add a new knowledge base entry."""
        self.knowledge_base[entry.entry_id] = entry
        logger.info(f"Added knowledge base entry: {entry.entry_id}")
    
    def update_case_status(self, case_id: str, status: str, resolution: Optional[str] = None):
        """Update troubleshooting case status."""
        if case_id not in self.troubleshooting_cases:
            raise ValueError(f"Case {case_id} not found")
        
        case = self.troubleshooting_cases[case_id]
        case.status = status
        case.updated_at = datetime.now().isoformat()
        
        if resolution:
            case.resolution = resolution
        
        logger.info(f"Updated case {case_id} status to {status}")
    
    def get_case_recommendations(self, case_id: str) -> List[TroubleshootingRecommendation]:
        """Get all recommendations for a case."""
        return [rec for rec in self.recommendations.values() if rec.case_id == case_id]
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        total_entries = len(self.knowledge_base)
        categories = defaultdict(int)
        total_usage = 0
        
        for entry in self.knowledge_base.values():
            categories[entry.category] += 1
            total_usage += entry.usage_count
        
        return {
            "total_entries": total_entries,
            "categories": dict(categories),
            "total_usage": total_usage,
            "average_success_rate": sum(entry.success_rate for entry in self.knowledge_base.values()) / total_entries if total_entries > 0 else 0
        }
    
    def save_knowledge_base(self, output_file: Optional[str] = None) -> Path:
        """Save knowledge base to JSON file."""
        if output_file is None:
            output_file = Path("/workspace/data") / "troubleshooting_knowledge_base.json"
        else:
            output_file = Path(output_file)
        
        kb_data = {
            "entries": [asdict(entry) for entry in self.knowledge_base.values()],
            "cases": [asdict(case) for case in self.troubleshooting_cases.values()],
            "recommendations": [asdict(rec) for rec in self.recommendations.values()],
            "saved_at": datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(kb_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved knowledge base to: {output_file}")
        return output_file
    
    def load_knowledge_base(self, input_file: Union[str, Path]):
        """Load knowledge base from JSON file."""
        input_file = Path(input_file)
        
        with open(input_file, 'r', encoding='utf-8') as f:
            kb_data = json.load(f)
        
        # Load entries
        for entry_data in kb_data.get("entries", []):
            entry = KnowledgeBaseEntry(**entry_data)
            self.knowledge_base[entry.entry_id] = entry
        
        # Load cases
        for case_data in kb_data.get("cases", []):
            case = TroubleshootingCase(**case_data)
            self.troubleshooting_cases[case.case_id] = case
        
        # Load recommendations
        for rec_data in kb_data.get("recommendations", []):
            rec = TroubleshootingRecommendation(**rec_data)
            self.recommendations[rec.recommendation_id] = rec
        
        logger.info(f"Loaded knowledge base from: {input_file}")
    
    def search_knowledge_base(self, query: str, limit: int = 10) -> List[KnowledgeBaseEntry]:
        """Search knowledge base entries."""
        query_lower = query.lower()
        results = []
        
        for entry in self.knowledge_base.values():
            score = 0
            
            # Check title match
            if query_lower in entry.title.lower():
                score += 3
            
            # Check content match
            if query_lower in entry.content.lower():
                score += 2
            
            # Check tag match
            for tag in entry.tags:
                if query_lower in tag.lower():
                    score += 1
            
            # Check error pattern match
            for pattern in entry.error_patterns:
                if query_lower in pattern.lower():
                    score += 2
            
            if score > 0:
                results.append((entry, score))
        
        # Sort by score and return top results
        results.sort(key=lambda x: x[1], reverse=True)
        return [entry for entry, score in results[:limit]]