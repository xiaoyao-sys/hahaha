"""
基金限额信息获取工具模块
专门用于获取基金申购限额信息
"""

import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any

class FundLimitFetcher:
    """基金限额信息获取器"""
    
    def __init__(self):
        """初始化基金限额信息获取器"""
        pass
    
    def get_fund_purchase_data(self) -> Optional[pd.DataFrame]:
        """
        获取基金申购数据，包含限额信息
        
        Returns:
            Optional[pd.DataFrame]: 基金申购数据，获取失败返回None
        """
        try:
            # 尝试获取基金申购数据
            fund_purchase_em_df = ak.fund_purchase_em()
            return fund_purchase_em_df
        except Exception as e:
            print(f"获取基金申购数据失败: {e}")
            # 如果akshare方法失败，返回None
            return None
    
    def extract_fund_limit_info(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """
        提取基金的限额信息
        
        Args:
            fund_code (str): 基金代码
            
        Returns:
            Optional[Dict[str, Any]]: 基金限额信息，获取失败返回None
                {
                    "limit_amount": float,      # 限额金额
                    "purchase_status": str,     # 申购状态
                    "fund_type": str,           # 基金类型
                    "fund_name": str            # 基金名称
                }
        """
        try:
            # 获取所有基金申购数据
            fund_data = self.get_fund_purchase_data()
            if fund_data is None:
                print(f"无法获取基金数据，基金代码: {fund_code}")
                return None
            
            # 检查数据框是否包含必要的列
            required_columns = ['基金代码']
            if not all(col in fund_data.columns for col in required_columns):
                print("基金数据缺少必要的列")
                return None
            
            # 首先尝试直接匹配基金代码
            fund_info = fund_data[fund_data['基金代码'] == fund_code]
            
            # 如果直接匹配失败，尝试去除前缀后匹配
            if fund_info.empty:
                # 提取数字部分
                numeric_code = fund_code[2:] if len(fund_code) > 2 else fund_code
                print(f"直接匹配失败，尝试使用数字部分匹配: {numeric_code}")
                fund_info = fund_data[fund_data['基金代码'].str.contains(numeric_code, na=False)]
            
            if fund_info.empty:
                print(f"未找到基金代码: {fund_code}")
                return None
            
            # 提取关键信息
            fund_row = fund_info.iloc[0]
            
            # 获取可用的列名
            columns = fund_row.index.tolist()
            
            # 安全地获取字段值
            limit_amount = fund_row.get('日累计限定金额', 0) if '日累计限定金额' in columns else 0
            purchase_status = fund_row.get('申购状态', '') if '申购状态' in columns else ''
            fund_type = fund_row.get('基金类型', '') if '基金类型' in columns else ''
            fund_name = fund_row.get('基金简称', '') if '基金简称' in columns else ''
            
            return {
                "limit_amount": float(limit_amount) if limit_amount else 0,
                "purchase_status": str(purchase_status) if purchase_status else '',
                "fund_type": str(fund_type) if fund_type else '',
                "fund_name": str(fund_name) if fund_name else ''
            }
        except Exception as e:
            print(f"提取基金 {fund_code} 限额信息失败: {e}")
            return None
    
    def fetch_fund_limit_info(self, fund_code: str) -> Optional[str]:
        """
        获取基金限额信息并格式化为显示文本
        
        Args:
            fund_code (str): 基金代码
            
        Returns:
            Optional[str]: 基金限额信息，格式化为显示文本
        """
        try:
            # 使用LOF数据获取器获取限额信息
            limit_info = self.extract_fund_limit_info(fund_code)
            if limit_info is None:
                return None
            
            purchase_status = limit_info.get("purchase_status", "")
            limit_amount = limit_info.get("limit_amount", 0)
            
            # 根据申购状态和限额金额生成显示文本
            if purchase_status == "暂停申购":
                return "暂停"
            elif limit_amount > 0:
                # 如果限额金额大于0，显示限额信息
                if limit_amount >= 10000:
                    return f"限{limit_amount/10000:.0f}万"
                else:
                    return f"限{limit_amount:.0f}"
            else:
                # 不限额或限额为0时不显示
                return ""
        except Exception as e:
            print(f"获取基金 {fund_code} 限额信息失败: {e}")
            return None

# 创建全局实例
fund_limit_fetcher = FundLimitFetcher()

# 便捷函数
def get_fund_limit(fund_code: str) -> Optional[str]:
    """
    获取基金限额信息的便捷函数
    
    Args:
        fund_code (str): 基金代码
        
    Returns:
        Optional[str]: 基金限额信息
    """
    return fund_limit_fetcher.fetch_fund_limit_info(fund_code)

def get_fund_limit_details(fund_code: str) -> Optional[Dict[str, Any]]:
    """
    获取基金详细限额信息的便捷函数
    
    Args:
        fund_code (str): 基金代码
        
    Returns:
        Optional[Dict[str, Any]]: 基金详细限额信息
    """
    return fund_limit_fetcher.extract_fund_limit_info(fund_code)