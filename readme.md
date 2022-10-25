# 자스트라바페라

> 사트 관리용 봇

**자스트라바페라**는 인공어 사전, 단어 생성기, 사트 역법 변환 등 기능을 제공하는 Discord 봇입니다.
[이 링크](https://discord.com/api/oauth2/authorize?client_id=944526568204681216&permissions=2147483648&scope=bot%20applications.commands)를
통해 자신의 서버에서 Zastravapera를 사용해볼 수 있습니다.

## 파라미터

```
usage: __main__.py [-h] [-t] [-c COG] [-o OVERRIDE]

options:
  -h, --help            도움말 메시지를 보여주고 종료합니다
  -t, --test            자스트라바페라 봇을 `test_bot_token`으로 실행합니다. 설정되지 않은 경우,
                        `bot_token`으로 실행합니다
  -c COG, --cog COG     이 정규표현식을 만족하는 이름을 가진 코그만 실행합니다
  -o OVERRIDE, --override OVERRIDE
                        const를 override합니다. `key=value`의 형태로 입력합니다.
```

## /diac 사용법

/diac 명령어는 키보드에서 입력 가능한 ASCII 문자들로 이루어진 문자열을
여러가지 다이어크리틱을 포함한 문자열로 바꿔주는 명령어입니다.
사용되는 기호들의 의미는 다음과 같습니다.

| 기호  | 의미                |
|-----|-------------------|
| !   | without           |
| ''  | acute             |
| "   | trema             |
| '   | acute             |
| -   | macron            |
| .   | dot above         |
| /   | stroke / slash    |
| :   | trema             |
| ;   | escape / ligature |
| ;o  | ring above        |
| ;u  | breve             |
| ;v  | caron             |
| ^   | circumflex        |
| ``  | double grave      |
| ~   | tilde             |

변환의 예시는 다음과 같습니다.

| 입력한 문자열            | 변환 결과             |
|--------------------|-------------------|
| `t;bows/od!i,c`    | `t͡sødıç`         |
| `Zasospik'ekomkos` | `Zasospikékomkos` |
| `'A~N^I;VS/K:A`    | `ÁÑÎŠꝀÄ`          |
