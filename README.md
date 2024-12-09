## flow chart
![image](https://github.com/user-attachments/assets/a7a36ded-8f60-49f5-8002-975dfbc7cff2)
<br/>
회원가입: SMTP방식을 사용하여 장고의 이메일 인증 토큰을 사용하여 자신의 계정이맞는지 확인
<br/>
로그인: ID,PW 검증후 JWT 액세스 토큰,리프레시 토큰 발급
<br/>
로그아웃: JWT "리프레시 토큰" Django Blacklist App에 등록
<br/>
## celery
### beat 터미널
![img.png](img.png)
### worker 터미널
![img_1.png](img_1.png)

