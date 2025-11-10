"""간단한 측정 및 CSV 로깅 예제

시나리오(예시)
--------------
- SCPI 명령으로 측정값(예: 전압 :MEAS:VOLT? 또는 :READ?)을 읽어옴
- N번 반복 측정한 뒤, CSV 파일로 저장

실제 명령어는 사용하는 계측기(제조사/모델)에 따라 다르므로,
아래 MEASURE_COMMAND 부분을 장비 매뉴얼 기준으로 수정해서 사용하세요.
"""

import csv
import time
from datetime import datetime

from instrument_base import InstrumentManager

# 한글 주석: 사용하는 계측기의 SCPI 측정 명령으로 변경해야 함
MEASURE_COMMAND = ":MEAS:VOLT?"  # 예시: 전압 측정
DEFAULT_REPEAT = 10
DEFAULT_INTERVAL_SEC = 1.0
DEFAULT_CSV_PATH = "measure_log.csv"


def main() -> None:
    manager = InstrumentManager()

    resources = manager.list_resources()
    if not resources:
        print("연결된 VISA 계측기가 없습니다.")
        return

    print("[VISA 리소스 목록]")
    for idx, r in enumerate(resources, start=1):
        print(f"{idx:02d}: {r}")

    print("\n측정을 수행할 장비 번호를 입력하세요 (예: 1):", end=" ")
    try:
        sel = int(input().strip())
    except ValueError:
        print("잘못된 입력입니다.")
        return

    if not (1 <= sel <= len(resources)):
        print("범위를 벗어난 번호입니다.")
        return

    resource_name = resources[sel - 1]
    inst = manager.open_scpi_instrument(resource_name)

    try:
        print(f"선택된 리소스: {resource_name}")
        print(f"측정 SCPI 명령: {MEASURE_COMMAND}")

        # 반복 횟수 설정
        print(f"반복 측정 횟수 입력 (기본값 {DEFAULT_REPEAT}):", end=" ")
        line = input().strip()
        repeat = int(line) if line else DEFAULT_REPEAT

        # 측정 간격 설정
        print(f"측정 간격(초) 입력 (기본값 {DEFAULT_INTERVAL_SEC}):", end=" ")
        line = input().strip()
        interval = float(line) if line else DEFAULT_INTERVAL_SEC

        # CSV 경로 설정
        print(f"CSV 저장 경로 입력 (기본값 {DEFAULT_CSV_PATH}):", end=" ")
        line = input().strip()
        csv_path = line if line else DEFAULT_CSV_PATH

        print(f"\n{repeat}회 측정을 시작합니다...")

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Index", "Timestamp", "RawValue"])

            for i in range(1, repeat + 1):
                ts = datetime.now().isoformat(timespec="seconds")
                try:
                    value = inst.query(MEASURE_COMMAND)
                except Exception as e:
                    print(f"[{i}] 측정 중 오류 발생: {e}")
                    value = "ERROR"

                writer.writerow([i, ts, value])
                print(f"[{i}/{repeat}] {ts} -> {value}")

                if i < repeat:
                    time.sleep(interval)

        print(f"\n측정 완료. CSV 파일: {csv_path}")

    finally:
        inst.close()


if __name__ == "__main__":
    main()
