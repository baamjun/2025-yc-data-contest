import requests
import pandas as pd
import urllib3

# SSL 경고 메시지 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class YeongcheonAPI:
    def __init__(self):
        # 인코딩된 서비스키 사용
        self.service_key = "WEqNavYxgpmVapYjluaVycOOkGUReVURSwkiOZDoKt0gO8%2FdrUhgMAiWiGNhoxY00GIzAsphmpfueL0du16l2Q%3D%3D"
        self.base_url = "https://apis.data.go.kr/5100000/yeongcheon_cctv1/getYeongcheonCctv"
    
    def get_cctv_data(self, page_no=1, num_of_rows=10):
        """CCTV 데이터를 가져오는 메서드"""
        params = {
            "serviceKey": self.service_key,
            "pageNo": page_no,
            "numOfRows": num_of_rows
        }
        
        try:
            # SSL 검증 비활성화
            response = requests.get(self.base_url, params=params, verify=False)
            
            # JSON 응답 파싱
            data = response.json()
            
            # 데이터 추출
            items = data['body']['items']['item']
            if not isinstance(items, list):
                items = [items]
            
            # DataFrame 생성
            df = pd.DataFrame(items)
            
            # 컬럼명 한글로 변경
            column_mapping = {
                'mng_inst_nm': '관리기관명',
                'lctn_road_addr_nm': '도로명주소',
                'lctn_lonto_addr': '지번주소',
                'instl_prps_se': '설치목적',
                'camera_cntom': '카메라방향',
                'camera_pixel_cnt': '카메라화소수',
                'potogrf_drc_info': '촬영방향정보',
                'cstdy_day_cnt': '보관일수',
                'instl_ym': '설치년월',
                'mng_inst_telno': '관리기관전화번호',
                'lat': '위도',
                'lot': '경도',
                'data_crtr_ymd': '데이터기준일자'
            }
            df = df.rename(columns=column_mapping)
            
            return df
            
        except Exception as e:
            print(f"오류 발생: {e}")
            return pd.DataFrame()

# 사용 예시
if __name__ == "__main__":
    # API 인스턴스 생성
    api = YeongcheonAPI()
    
    # CCTV 데이터 가져오기
    cctv_df = api.get_cctv_data(page_no=1, num_of_rows=100)
    
    # 데이터 확인
    if not cctv_df.empty:
        print("\n=== 영천시 CCTV 데이터 ===")
        print(f"총 {len(cctv_df)}개의 CCTV 정보가 있습니다.")
        print("\n=== 데이터 미리보기 ===")
        print(cctv_df.head())
    else:
        print("데이터를 가져오는데 실패했습니다.") 