"""
제품 및 HS 코드 관련 데이터베이스
"""

# 제품별 HS 코드 매핑 데이터
PRODUCT_HS_MAPPING = {
    # 견과류
    'macadamia': {
        'name': '마카다미아',
        'codes': [
            {'code': '080250', 'description': '마카다미아 너트 (껍질 있음)'},
            {'code': '080251', 'description': '마카다미아 너트 (껍질 없음)'}
        ]
    },
    'almond': {
        'name': '아몬드',
        'codes': [
            {'code': '080211', 'description': '아몬드 (껍질 있음, 생것)'},
            {'code': '080212', 'description': '아몬드 (껍질 없음, 생것)'}
        ]
    },
    'walnut': {
        'name': '호두',
        'codes': [
            {'code': '080231', 'description': '호두 (껍질 있음)'},
            {'code': '080232', 'description': '호두 (껍질 없음)'}
        ]
    },
    'cashew': {
        'name': '캐슈넛',
        'codes': [
            {'code': '080131', 'description': '캐슈넛 (껍질 있음)'},
            {'code': '080132', 'description': '캐슈넛 (껍질 없음)'}
        ]
    },
    'pistachio': {
        'name': '피스타치오',
        'codes': [
            {'code': '080251', 'description': '피스타치오 (껍질 있음)'},
            {'code': '080252', 'description': '피스타치오 (껍질 없음)'}
        ]
    },
    
    # 과일류
    'apple': {
        'name': '사과',
        'codes': [
            {'code': '080810', 'description': '사과 (신선한 것)'},
            {'code': '200979', 'description': '사과 주스'}
        ]
    },
    'banana': {
        'name': '바나나',
        'codes': [
            {'code': '080300', 'description': '바나나 (신선한 것 또는 건조한 것)'}
        ]
    },
    'orange': {
        'name': '오렌지',
        'codes': [
            {'code': '080510', 'description': '오렌지 (신선한 것)'},
            {'code': '200911', 'description': '오렌지 주스 (냉동하지 않은 것)'}
        ]
    },
    'grape': {
        'name': '포도',
        'codes': [
            {'code': '080610', 'description': '포도 (신선한 것)'},
            {'code': '080620', 'description': '포도 (건조한 것)'}
        ]
    },
    
    # 곡물류
    'rice': {
        'name': '쌀',
        'codes': [
            {'code': '100630', 'description': '쌀 (현미)'},
            {'code': '100640', 'description': '쌀 (부서진 것)'}
        ]
    },
    'wheat': {
        'name': '밀',
        'codes': [
            {'code': '100111', 'description': '밀 (종자용 듀럼밀)'},
            {'code': '100119', 'description': '밀 (기타 듀럼밀)'},
            {'code': '100191', 'description': '밀 (기타, 종자용)'},
            {'code': '100199', 'description': '밀 (기타)'}
        ]
    },
    'corn': {
        'name': '옥수수',
        'codes': [
            {'code': '100510', 'description': '옥수수 (종자용)'},
            {'code': '100590', 'description': '옥수수 (기타)'}
        ]
    },
    
    # 육류
    'beef': {
        'name': '쇠고기',
        'codes': [
            {'code': '020110', 'description': '쇠고기 (뼈가 있는 것, 신선한 것 또는 냉장한 것)'},
            {'code': '020120', 'description': '쇠고기 (뼈가 없는 것, 신선한 것 또는 냉장한 것)'},
            {'code': '020210', 'description': '쇠고기 (뼈가 있는 것, 냉동한 것)'},
            {'code': '020220', 'description': '쇠고기 (뼈가 없는 것, 냉동한 것)'}
        ]
    },
    'pork': {
        'name': '돼지고기',
        'codes': [
            {'code': '020311', 'description': '돼지고기 (통째 또는 반분한 것, 신선한 것 또는 냉장한 것)'},
            {'code': '020312', 'description': '돼지고기 (다리살과 어깨살, 신선한 것 또는 냉장한 것)'}
        ]
    },
    
    # 수산물
    'salmon': {
        'name': '연어',
        'codes': [
            {'code': '030212', 'description': '연어 (신선한 것 또는 냉장한 것)'},
            {'code': '030312', 'description': '연어 (냉동한 것)'}
        ]
    },
    'tuna': {
        'name': '참치',
        'codes': [
            {'code': '030232', 'description': '참치 (신선한 것 또는 냉장한 것)'},
            {'code': '030332', 'description': '참치 (냉동한 것)'}
        ]
    },
    
    # 차류
    'coffee': {
        'name': '커피',
        'codes': [
            {'code': '090111', 'description': '커피 (볶지 않은 것, 카페인을 제거하지 않은 것)'},
            {'code': '090112', 'description': '커피 (볶지 않은 것, 카페인을 제거한 것)'},
            {'code': '090121', 'description': '커피 (볶은 것, 카페인을 제거하지 않은 것)'},
            {'code': '090122', 'description': '커피 (볶은 것, 카페인을 제거한 것)'}
        ]
    },
    'tea': {
        'name': '차',
        'codes': [
            {'code': '090210', 'description': '녹차 (발효하지 않은 것)'},
            {'code': '090220', 'description': '기타 차 (발효한 것)'},
            {'code': '090230', 'description': '홍차 (발효한 것)'}
        ]
    }
}

# HS 코드별 관세 및 규제 정보
HS_CODE_INFO = {
    # 마카다미아
    '080250': {
        'tariff_rate': '8%',
        'import_regulations': [
            '식물검역증명서 필수',
            '잔류농약 검사 대상',
            '수입신고서 제출 필요'
        ],
        'precautions': [
            '수입 시 검역소 사전 신고 필요',
            '포장재 소독 처리 필수',
            '유통기한 표시 의무',
            '알레르기 유발 가능 식품으로 표시 필요'
        ],
        'additional_info': {
            'origin_requirements': '원산지 증명서 필요',
            'storage_conditions': '건조하고 서늘한 곳 보관',
            'shelf_life': '일반적으로 12개월',
            'market_info': '프리미엄 견과류로 고가 시장 형성'
        }
    },
    '080251': {
        'tariff_rate': '8%',
        'import_regulations': [
            '식물검역증명서 필수',
            '잔류농약 검사 대상',
            '수입신고서 제출 필요'
        ],
        'precautions': [
            '수입 시 검역소 사전 신고 필요',
            '포장재 소독 처리 필수',
            '유통기한 표시 의무',
            '알레르기 유발 가능 식품으로 표시 필요'
        ],
        'additional_info': {
            'origin_requirements': '원산지 증명서 필요',
            'storage_conditions': '밀폐 포장, 냉장 보관 권장',
            'shelf_life': '껍질 제거로 인해 6-8개월',
            'market_info': '가공식품 원료로 많이 사용'
        }
    },
    
    # 아몬드
    '080211': {
        'tariff_rate': '5%',
        'import_regulations': [
            '식물검역증명서 필수',
            '아플라톡신 검사 대상'
        ],
        'precautions': [
            '곰팡이독소 검사 필수',
            '수분 함량 관리 중요',
            '알레르기 표시 의무'
        ],
        'additional_info': {
            'origin_requirements': '주요 수입국: 미국, 호주',
            'storage_conditions': '습도 65% 이하 유지',
            'market_info': '견과류 시장의 대표 품목'
        }
    },
    '080212': {
        'tariff_rate': '5%',
        'import_regulations': [
            '식물검역증명서 필수',
            '아플라톡신 검사 대상'
        ],
        'precautions': [
            '곰팡이독소 검사 필수',
            '산패 방지를 위한 포장 중요',
            '알레르기 표시 의무'
        ],
        'additional_info': {
            'origin_requirements': '주요 수입국: 미국, 호주',
            'storage_conditions': '진공포장 또는 질소충전 포장',
            'market_info': '가공식품 및 제과용으로 인기'
        }
    },
    
    # 커피
    '090111': {
        'tariff_rate': '2%',
        'import_regulations': [
            '식품안전관리인증기준(HACCP) 적용',
            '잔류농약 검사'
        ],
        'precautions': [
            '곰팡이독소(오크라톡신A) 검사',
            '품질등급 확인 필요',
            '수분함량 12% 이하 유지'
        ],
        'additional_info': {
            'origin_requirements': '원산지별 관세율 차등 적용',
            'storage_conditions': '통풍이 잘 되는 건조한 곳',
            'market_info': '스페셜티 커피 시장 확대 중'
        }
    },
    
    # 쇠고기
    '020110': {
        'tariff_rate': '40%',
        'import_regulations': [
            '수의위생증명서 필수',
            'BSE 안전성 확인',
            '동물검역증명서'
        ],
        'precautions': [
            '냉장 유통체계 필수 (-2°C ~ 4°C)',
            '할랄 인증 필요시 별도 처리',
            '유통기한 엄격 관리'
        ],
        'additional_info': {
            'origin_requirements': 'FTA 협정국 우대관세 적용',
            'storage_conditions': '냉장 보관, 교차오염 방지',
            'market_info': '프리미엄 부위별 가격 차이 큼'
        }
    },
    
    # 연어
    '030212': {
        'tariff_rate': '10%',
        'import_regulations': [
            '수산물 위생증명서',
            '방사능 검사',
            '항생제 잔류검사'
        ],
        'precautions': [
            '냉장 유통 (-1°C ~ 4°C)',
            '신선도 관리 중요',
            '원료 어종 확인'
        ],
        'additional_info': {
            'origin_requirements': '노르웨이, 칠레산 주요 수입',
            'storage_conditions': '즉시 냉장/냉동 보관',
            'market_info': '양식산과 자연산 가격 차이'
        }
    }
}

def search_products_by_name(query: str) -> list:
    """제품명으로 HS 코드 검색"""
    results = []
    query_lower = query.lower()
    
    for key, product in PRODUCT_HS_MAPPING.items():
        if (query_lower in key.lower() or 
            query_lower in product['name'].lower() or
            any(query_lower in code['description'].lower() for code in product['codes'])):
            results.append({
                'key': key,
                'name': product['name'],
                'codes': product['codes']
            })
    
    return results

def get_hs_code_info(hs_code: str) -> dict:
    """HS 코드 상세 정보 조회"""
    return HS_CODE_INFO.get(hs_code, {
        'tariff_rate': '정보 없음',
        'import_regulations': ['상세 정보 없음'],
        'precautions': ['해당 품목 관련 규정 확인 필요'],
        'additional_info': {
            'origin_requirements': '관세청 또는 관련 기관 문의',
            'storage_conditions': '제품별 보관 조건 확인',
            'market_info': '시장 동향 별도 조사 필요'
        }
    })

def get_all_product_categories():
    """모든 제품 카테고리 반환"""
    categories = {
        '견과류': ['macadamia', 'almond', 'walnut', 'cashew', 'pistachio'],
        '과일류': ['apple', 'banana', 'orange', 'grape'],
        '곡물류': ['rice', 'wheat', 'corn'],
        '육류': ['beef', 'pork'],
        '수산물': ['salmon', 'tuna'],
        '차류': ['coffee', 'tea']
    }
    
    result = {}
    for category, items in categories.items():
        result[category] = []
        for item in items:
            if item in PRODUCT_HS_MAPPING:
                result[category].append({
                    'key': item,
                    'name': PRODUCT_HS_MAPPING[item]['name']
                })
    
    return result
