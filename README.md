<h1>Fullstack Service Networking Season.2 <br />Simple Loopback Client & Server Program</h1>	

Server : Python (aioquic)

Client : Python (aioquic)

Networking : HTTP/3 (QUIC)

Packaging : Poetry (추가 패키지: aioquic)

<br />
<br />

<h2>실행 방법</h2>	

프로젝트를 다운로드 함

폴더안에서 poetry shell를 실행함<br />
> poetry shell

폴더안에서 필요한 패키지를 설치함<br />
> poetry install

src/server.py를 실행함<br />
> python server.py --certificate ../cert/server.crt --private-key ../cert/server.key --port 8053

src/client.py를 실행함<br />
> python client.py --ca-certs ../cert/server.crt --port 8053

<br />
<br />

<h2>수정 방법</h2>	

Server
> step.1: 개발할 프로토콜을 lib/server_lib_loopbackprotocol.py 처럼 개발함
> step.2: server.py 코드의 [SHOULD BE MODIFIED] 부분을 step.1에 맞춰서 수정함
> step.3: 코드를 실행함

Client 
> step.1: 개발할 프로토콜을 lib/client_lib_loopbackprotocol.py 처럼 개발함
> step.2: client.py 코드의 [SHOULD BE MODIFIED] 부분을 step.1에 맞춰서 수정함
> step.3: 코드를 실행함

<br />
<br />

<h2>실행 화면</h2>	

<img src="/screen/server.png" width="1000"/>

<img src="/screen/client.png" width="1000"/>