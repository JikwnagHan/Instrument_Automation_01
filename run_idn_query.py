"""사용자가 선택한 VISA 리소스에 *IDN? 을 보내고 응답을 출력하는 예제

사용 방법
--------
1) 연결된 장비 목록 확인:
   python run_list_resources.py
2) 아래 스크립트 실행:
   python run_idn_query.py
"""

from instrument_base import InstrumentManager


def main() -> None:
    manager = InstrumentManager()  # 필요시 backend='@py' 사용

    resources = manager.list_resources()
    if not resources:
        print("연결된 VISA 계측기가 없습니다.")
        return

    print("[VISA 리소스 목록]")
    for idx, r in enumerate(resources, start=1):
        print(f"{idx:02d}: {r}")

    print("\n사용할 장비 번호를 입력하세요 (예: 1):", end=" ")
    try:
        sel = int(input().strip())
    except ValueError:
        print("잘못된 입력입니다.")
        return

    if not (1 <= sel <= len(resources)):
        print("범위를 벗어난 번호입니다.")
        return

    resource_name = resources[sel - 1]
    print(f"선택된 리소스: {resource_name}")

    inst = manager.open_scpi_instrument(resource_name)
    try:
        idn = inst.idn()
        print("\n[*IDN? 응답]")
        print(idn)
    finally:
        inst.close()


if __name__ == "__main__":
    main()
