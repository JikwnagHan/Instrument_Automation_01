import pyvisa

class InstrumentManager:
    """VISA 리소스 매니저를 래핑한 간단한 헬퍼 클래스.

    - 연결 가능한 계측기 목록 조회
    - 특정 리소스 문자열로 계측기 객체 생성
    """

    def __init__(self, backend: str | None = None) -> None:
        """VISA ResourceManager 초기화

        backend:
            - None  : 기본 VISA 라이브러리 사용 (예: NI-VISA)
            - '@py' : PyVISA-py 백엔드 사용 (드라이버 없이 순수 파이썬)
        """
        # 한글 주석: backend 인자를 통해 실제 하드웨어 드라이버 방식 선택
        if backend:
            self.rm = pyvisa.ResourceManager(backend)
        else:
            self.rm = pyvisa.ResourceManager()

    def list_resources(self) -> list[str]:
        """현재 연결된 VISA 리소스 목록을 반환"""
        return list(self.rm.list_resources())

    def open_scpi_instrument(self, resource_name: str, timeout_ms: int = 5000):
        """SCPI 기반 계측기 리소스를 열어 ScpiInstrument 객체를 반환"""
        inst = self.rm.open_resource(resource_name)
        inst.timeout = timeout_ms
        return ScpiInstrument(inst)


class ScpiInstrument:
    """SCPI 프로토콜 기반 계측기를 추상화한 래퍼 클래스.

    대부분의 벤치형 계측기(오실로스코프, DMM, PSU 등)는 SCPI 명령을 지원합니다.
    이 클래스는 PyVISA 오브젝트를 감싸서, 조금 더 직관적인 메서드를 제공합니다.
    """

    def __init__(self, visa_inst) -> None:
        # 한글 주석: visa_inst 는 ResourceManager.open_resource() 결과 객체
        self._inst = visa_inst

    def write(self, cmd: str) -> None:
        """SCPI 명령 전송 (질의 응답 필요 없는 경우)"""
        self._inst.write(cmd)

    def read(self) -> str:
        """장비로부터 문자열 응답을 한 번 읽어옴"""
        return self._inst.read()

    def query(self, cmd: str) -> str:
        """SCPI 질의 명령 전송 후, 단일 문자열 응답을 반환"""
        return self._inst.query(cmd).strip()

    def idn(self) -> str:
        """표준 *IDN? 명령으로 장비 모델/제조사/버전 조회"""
        return self.query("*IDN?")

    def close(self) -> None:
        """VISA 세션 종료"""
        try:
            self._inst.close()
        except Exception:
            # 종료 중 예외는 치명적이지 않으므로 무시
            pass
