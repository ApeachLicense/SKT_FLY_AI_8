# Python 기초 예제

| 경로 | 내용 |
| --- | --- |
| `requests_version.py` | Requests 버전 확인 |
| `mysql_query.py` | MySQL 연결 및 테이블 조회 실습; 연결 값을 먼저 설정 |
| `streamlit_examples/hello_streamlit.py` | Streamlit 텍스트 출력 |
| `streamlit_examples/line_chart.py` | 임의 데이터 선 그래프 |
| `streamlit_examples/dataframe.py` | 데이터프레임 표시 |
| `streamlit_examples/map_points.py` | 지도에 임의 좌표 표시 |
| `streamlit_examples/number_guessing_game.py` | 세션 상태를 사용하는 숫자 맞히기 게임 |

저장소 루트에서 실행합니다.

```powershell
python -m pip install streamlit pandas numpy
python -m streamlit run python_basics/streamlit_examples/line_chart.py
```

HTTP 요청 실습은 [Azure 폴더의 예제](../cloud_azure/python-http-sample/fetch_web_page.py), PyTorch 실습은 [deep_learning](../deep_learning/)에 있습니다.
