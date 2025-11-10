계측기 자동화 예제 (Python + PyVISA)
====================================

1. Python 환경 준비
   - Python 3.9 이상 설치
   - 가상환경(선택) 생성 후 활성화

2. 필수 라이브러리 설치
   - 이 폴더에서 다음 명령 실행:
     pip install -r requirements.txt

3. NI-VISA 또는 PyVISA-py 백엔드 준비
   - 물리 장비를 NI-VISA로 제어: NI-VISA 드라이버 설치
   - 또는, 드라이버 설치 없이 PyVISA-py 사용 가능

4. 예제 실행
   - 연결된 계측기 목록 확인:
     python run_list_resources.py
   - 특정 장비에 접속해서 *IDN? 질의:
     python run_idn_query.py
   - 간단 측정값(예: 전압) 반복 측정 및 CSV 로깅:
     python run_measure_and_log.py

주의사항
--------
- 실제 VISA 리소스 문자열(예: 'USB0::0x1AB1::0x04CE::DS1ZA170000001::INSTR')은
  각 장비/드라이버 환경에 따라 다르므로, run_list_resources.py 결과를 참고해서
  사용하세요.
