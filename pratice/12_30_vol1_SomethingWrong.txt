Windows PowerShell

Copyright (C) Microsoft Corporation. All rights reserved.



새로운 기능 및 개선 사항에 대 한 최신 PowerShell을 설치 하세요! https://aka.ms/PSWindows



(.venv) PS C:\Users\jwkim\PyCharmMiscProject> !pip install ipykernel

!pip : '!pip' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다. 이름이 정확한지 확인하고 경로가 포함된 경우 경로가 올바른지

검증한 다음 다시 시도하십시오.

위치 줄:1 문자:1

+ !pip install ipykernel

+ ~~~~

+ CategoryInfo : ObjectNotFound: (!pip:String) [], CommandNotFoundException

+ FullyQualifiedErrorId : CommandNotFoundException


(.venv) PS C:\Users\jwkim\PyCharmMiscProject> pip install langchain

Collecting langchain

Using cached langchain-1.2.0-py3-none-any.whl.metadata (4.9 kB)

Collecting langchain-core<2.0.0,>=1.2.1 (from langchain)

Using cached langchain_core-1.2.5-py3-none-any.whl.metadata (3.7 kB)

Collecting langgraph<1.1.0,>=1.0.2 (from langchain)

Using cached langgraph-1.0.5-py3-none-any.whl.metadata (7.4 kB)

Collecting pydantic<3.0.0,>=2.7.4 (from langchain)

Using cached pydantic-2.12.5-py3-none-any.whl.metadata (90 kB)

Collecting jsonpatch<2.0.0,>=1.33.0 (from langchain-core<2.0.0,>=1.2.1->langchain)

Using cached jsonpatch-1.33-py2.py3-none-any.whl.metadata (3.0 kB)

Collecting langsmith<1.0.0,>=0.3.45 (from langchain-core<2.0.0,>=1.2.1->langchain)

Using cached langsmith-0.5.1-py3-none-any.whl.metadata (15 kB)

Collecting packaging<26.0.0,>=23.2.0 (from langchain-core<2.0.0,>=1.2.1->langchain)

Using cached packaging-25.0-py3-none-any.whl.metadata (3.3 kB)

Collecting pyyaml<7.0.0,>=5.3.0 (from langchain-core<2.0.0,>=1.2.1->langchain)

Using cached pyyaml-6.0.3.tar.gz (130 kB)

Installing build dependencies ... done

Getting requirements to build wheel ... done

Preparing metadata (pyproject.toml) ... done

Collecting tenacity!=8.4.0,<10.0.0,>=8.1.0 (from langchain-core<2.0.0,>=1.2.1->langchain)

Using cached tenacity-9.1.2-py3-none-any.whl.metadata (1.2 kB)

Collecting typing-extensions<5.0.0,>=4.7.0 (from langchain-core<2.0.0,>=1.2.1->langchain)

Using cached typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)

Collecting uuid-utils<1.0,>=0.12.0 (from langchain-core<2.0.0,>=1.2.1->langchain)

Using cached uuid_utils-0.12.0.tar.gz (20 kB)

Installing build dependencies ... error

error: subprocess-exited-with-error


× pip subprocess to install build dependencies did not run successfully.

│ exit code: 1

╰─> [30 lines of output]

Collecting maturin<2,>=1

Using cached maturin-1.10.2.tar.gz (217 kB)

Installing build dependencies: started

Installing build dependencies: finished with status 'done'

Getting requirements to build wheel: started

Getting requirements to build wheel: finished with status 'done'

Installing backend dependencies: started

Installing backend dependencies: finished with status 'done'

Preparing metadata (pyproject.toml): started

Preparing metadata (pyproject.toml): finished with status 'error'

error: subprocess-exited-with-error


Preparing metadata (pyproject.toml) did not run successfully.

exit code: 1


[3 lines of output]

Python reports SOABI: cpython-312

Unsupported platform: 312

Rust not found, installing into a temporary directory

[end of output]


note: This error originates from a subprocess, and is likely not a problem with pip.

error: metadata-generation-failed


Encountered error while generating package metadata.


See above for output.


note: This is an issue with the package mentioned above, not pip.

hint: See above for details.

[end of output]


note: This error originates from a subprocess, and is likely not a problem with pip.



[notice] A new release of pip is available: 25.1.1 -> 25.3

[notice] To update, run: python.exe -m pip install --upgrade pip

error: subprocess-exited-with-error



× pip subprocess to install build dependencies did not run successfully.

│ exit code: 1

╰─> See above for output.



note: This error originates from a subprocess, and is likely not a problem with pip.

(.venv) PS C:\Users\jwkim\PyCharmMiscProject> pip install langchain-core langchain-community

Collecting langchain-core

Using cached langchain_core-1.2.5-py3-none-any.whl.metadata (3.7 kB)

Collecting langchain-community

Downloading langchain_community-0.4.1-py3-none-any.whl.metadata (3.0 kB)

Collecting jsonpatch<2.0.0,>=1.33.0 (from langchain-core)

Using cached jsonpatch-1.33-py2.py3-none-any.whl.metadata (3.0 kB)

Collecting langsmith<1.0.0,>=0.3.45 (from langchain-core)

Using cached langsmith-0.5.1-py3-none-any.whl.metadata (15 kB)

Collecting packaging<26.0.0,>=23.2.0 (from langchain-core)

Using cached packaging-25.0-py3-none-any.whl.metadata (3.3 kB)

Collecting pydantic<3.0.0,>=2.7.4 (from langchain-core)

Using cached pydantic-2.12.5-py3-none-any.whl.metadata (90 kB)

Collecting pyyaml<7.0.0,>=5.3.0 (from langchain-core)

Using cached pyyaml-6.0.3.tar.gz (130 kB)

Installing build dependencies ... done

Getting requirements to build wheel ... done

Preparing metadata (pyproject.toml) ... done

Collecting tenacity!=8.4.0,<10.0.0,>=8.1.0 (from langchain-core)

Using cached tenacity-9.1.2-py3-none-any.whl.metadata (1.2 kB)

Collecting typing-extensions<5.0.0,>=4.7.0 (from langchain-core)

Using cached typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)

Collecting uuid-utils<1.0,>=0.12.0 (from langchain-core)

Using cached uuid_utils-0.12.0.tar.gz (20 kB)

Installing build dependencies ... error

error: subprocess-exited-with-error


× pip subprocess to install build dependencies did not run successfully.

│ exit code: 1

╰─> [30 lines of output]

Collecting maturin<2,>=1

Using cached maturin-1.10.2.tar.gz (217 kB)

Installing build dependencies: started

Installing build dependencies: finished with status 'done'

Getting requirements to build wheel: started

Getting requirements to build wheel: finished with status 'done'

Installing backend dependencies: started

Installing backend dependencies: finished with status 'done'

Preparing metadata (pyproject.toml): started

Preparing metadata (pyproject.toml): finished with status 'error'

error: subprocess-exited-with-error


Preparing metadata (pyproject.toml) did not run successfully.

exit code: 1


[3 lines of output]

Python reports SOABI: cpython-312

Unsupported platform: 312

Rust not found, installing into a temporary directory

[end of output]


note: This error originates from a subprocess, and is likely not a problem with pip.

error: metadata-generation-failed


Encountered error while generating package metadata.


See above for output.


note: This is an issue with the package mentioned above, not pip.

hint: See above for details.

[end of output]


note: This error originates from a subprocess, and is likely not a problem with pip.



[notice] A new release of pip is available: 25.1.1 -> 25.3

[notice] To update, run: python.exe -m pip install --upgrade pip

error: subprocess-exited-with-error



× pip subprocess to install build dependencies did not run successfully.

│ exit code: 1

╰─> See above for output.



note: This error originates from a subprocess, and is likely not a problem with pip.
