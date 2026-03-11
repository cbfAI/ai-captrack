"""
热度评估服务

实现多维度热度评估算法:
heat_score = base_score * time_decay * source_weight + feedback_bonus

其中:
- base_score: 基础分数 (stars/downloads/usage)
- time_decay: 时间衰减因子 (0.5 ~ 1.0)
- source_weight: 来源权重 (github: 1.0, huggingface: 0.9, openrouter: 0.8)
- feedback_bonus: 反馈加成 (thumbs_up * 10 - thumbs_down * 5)
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum

from app.models.models import CapabilitySource


class HeatTrend(str, Enum):
    """热度趋势枚举"""
    RISING = "rising"      # 上升
    STABLE = "stable"      # 稳定
    DECLINING = "declining"  # 下降


class HeatScoreConfig:
    """热度评估配置"""
    # 来源权重
    SOURCE_WEIGHTS: Dict[str, float] = {
        "github": 1.0,
        "huggingface": 0.9,
        "openrouter": 0.8,
        "futuretools": 0.7,
    }
    
    # 反馈权重
    THUMBS_UP_WEIGHT: float = 10.0
    THUMBS_DOWN_WEIGHT: float = 5.0
    
    # 时间衰减配置
    TIME_DECAY_HALF_LIFE_DAYS: int = 90  # 90天衰减一半
    MIN_TIME_DECAY: float = 0.5  # 最小衰减因子
    
    # 热度趋势阈值
    TREND_RISING_THRESHOLD: float = 0.1    # 增长 10% 视为上升
    TREND_DECLINING_THRESHOLD: float = -0.1  # 下降 10% 视为下降
    
    @classmethod
    def get_source_weight(cls, source: str) -> float:
        """获取来源权重"""
        return cls.SOURCE_WEIGHTS.get(source.lower(), 0.7)
    
    @classmethod
    def set_source_weight(cls, source: str, weight: float):
        """设置来源权重"""
        cls.SOURCE_WEIGHTS[source.lower()] = weight


class HeatScoreService:
    """热度评估服务"""
    
    def __init__(self, config: HeatScoreConfig = None):
        self.config = config or HeatScoreConfig()
    
    def calculate_base_score(
        self,
        stars: int = 0,
        downloads: int = 0,
        usage_count: int = 0,
        source: str = "",
    ) -> float:
        """
        计算基础分数
        
        不同数据源使用不同指标:
        - GitHub: stars
        - HuggingFace: downloads
        - OpenRouter: usage_count
        """
        source_lower = source.lower() if source else ""
        
        if source_lower == "github":
            return float(stars)
        elif source_lower == "huggingface":
            return downloads / 1000.0  # 下载量转换
        elif source_lower == "openrouter":
            return usage_count / 100.0  # 使用量转换
        else:
            # 默认使用 stars
            return float(stars)
    
    def calculate_time_decay(
        self,
        updated_at: datetime,
        reference_time: datetime = None,
    ) -> float:
        """
        计算时间衰减因子
        
        使用指数衰减模型:
        decay = 2^(-elapsed_days / half_life)
        
        结果范围: [MIN_TIME_DECAY, 1.0]
        """
        if reference_time is None:
            reference_time = datetime.utcnow()
        
        if updated_at is None:
            return 1.0
        
        elapsed_days = (reference_time - updated_at).days
        if elapsed_days <= 0:
            return 1.0
        
        # 指数衰减
        half_life = self.config.TIME_DECAY_HALF_LIFE_DAYS
        decay = 2 ** (-elapsed_days / half_life)
        
        # 限制最小值
        return max(decay, self.config.MIN_TIME_DECAY)
    
    def calculate_feedback_bonus(
        self,
        thumbs_up: int = 0,
        thumbs_down: int = 0,
    ) -> float:
        """
        计算反馈加成
        
        bonus = thumbs_up * 10 - thumbs_down * 5
        """
        bonus = (
            thumbs_up * self.config.THUMBS_UP_WEIGHT -
            thumbs_down * self.config.THUMBS_DOWN_WEIGHT
        )
        return max(bonus, 0.0)  # 反馈加成不低于 0
    
    def calculate_heat_score(
        self,
        source: str,
        stars: int = 0,
        downloads: int = 0,
        usage_count: int = 0,
        updated_at: datetime = None,
        thumbs_up: int = 0,
        thumbs_down: int = 0,
    ) -> float:
        """
        计算综合热度分数
        
        heat_score = base_score * time_decay * source_weight + feedback_bonus
        """
        # 1. 基础分数
        base_score = self.calculate_base_score(
            stars=stars,
            downloads=downloads,
            usage_count=usage_count,
            source=source,
        )
        
        # 2. 时间衰减
        time_decay = self.calculate_time_decay(updated_at)
        
        # 3. 来源权重
        source_weight = self.config.get_source_weight(source)
        
        # 4. 反馈加成
        feedback_bonus = self.calculate_feedback_bonus(
            thumbs_up=thumbs_up,
            thumbs_down=thumbs_down,
        )
        
        # 5. 综合热度分数
        heat_score = base_score * time_decay * source_weight + feedback_bonus
        
        return round(heat_score, 2)
    
    def calculate_trend(
        self,
        current_score: float,
        previous_score: float,
    ) -> HeatTrend:
        """
        计算热度趋势
        
        增长率 = (current - previous) / previous
        """
        if previous_score == 0:
            return HeatTrend.STABLE
        
        change_rate = (current_score - previous_score) / previous_score
        
        if change_rate >= self.config.TREND_RISING_THRESHOLD:
            return HeatTrend.RISING
        elif change_rate <= self.config.TREND_DECLINING_THRESHOLD:
            return HeatTrend.DECLINING
        else:
            return HeatTrend.STABLE
    
    def update_heat_score(
        self,
        capability: Any,
        thumbs_up: int = None,
        thumbs_down: int = None,
    ) -> float:
        """
        更新单个能力的热度分数
        """
        # 获取反馈数据
        if thumbs_up is None:
            thumbs_up = getattr(capability, 'thumbs_up', 0) or 0
        if thumbs_down is None:
            thumbs_down = getattr(capability, 'thumbs_down', 0) or 0
        
        # 从 metadata 获取额外数据
        metadata = getattr(capability, 'metadata_', {}) or {}
        downloads = metadata.get('downloads', 0) or 0
        usage_count = metadata.get('usage_count', 0) or 0
        
        return self.calculate_heat_score(
            source=capability.source.value if hasattr(capability.source, 'value') else str(capability.source),
            stars=capability.stars or 0,
            downloads=downloads,
            usage_count=usage_count,
            updated_at=capability.updated_at,
            thumbs_up=thumbs_up,
            thumbs_down=thumbs_down,
        )


# 全局实例
heat_score_service = HeatScoreService()
