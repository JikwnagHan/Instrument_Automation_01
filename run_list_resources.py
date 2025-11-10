"""연결된 VISA 리소스 목록을 출력하는 간단한 스크립트

사용 방법
--------
python run_list_resources.py
"""

from instrument_base import InstrumentManager


def main() -> None:
    # 한글 주석: backend='@py' 로 설정하면 PyVISA-py 백엔드를 사용 (드라이버 설치 없이 테스트 가능)
    manager = InstrumentManager()  # 또는 InstrumentManager(backend='@py')
    resources = manager.list_resources()

    if not resources:
        print("연결된 VISA 계측기를 찾을 수 없습니다.")
        print("- NI-VISA 또는 pyvisa-py 설정을 확인하세요.")
        print("- USB/GPIB/LAN 케이블 및 장비 전원을 확인하세요.")
        return

    print("[VISA 리소스 목록]")
    for idx, r in enumerate(resources, start=1):
        print(f"{idx:02d}: {r}")


if __name__ == "__main__":
    main()
