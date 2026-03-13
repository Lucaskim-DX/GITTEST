<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# 안티그래비티 노트븍lm 연동방법

안티그래비티(Antigravity)와 노트북LM(NotebookLM)을 MCP(Model Context Protocol)를 통해 연동하면, 노트북LM의 지식 베이스를 Antigravity 에이전트에서 직접 활용할 수 있습니다. 주요 방법은 MCP 서버 설치와 스킬 추가 두 가지입니다.[^1][^2][^3]

## MCP 서버 설치

터미널에서 Python 설치 후 `pip install notebooklm-mcp-cli` 명령어를 실행합니다. Antigravity의 `mcp_config.json` 파일에 다음을 추가하세요:

```
"notebooklm-mcp": {
  "command": "notebooklm-mcp",
  "args": []
}
```

`nlm login`으로 Google 계정 인증 후, Antigravity에서 MCP 서버 목록을 새로고침하면 노트북LM이 연결됩니다.[^1]

## 스킬 추가 방법

GitHub 저장소 `https://github.com/sickn33/antigravity-awesome-skills`를 Antigravity에 클론합니다. 노트북LM 관련 스킬(예: notebooklm 스킬)을 드래그해 채팅에 추가하고, "@노트북이름"으로 지식 베이스를 지정해 사용하세요.[^4][^2][^3]

## 활용 예시

연동 후 "K-IFRS 회계기준 노트북에서 리스부채 재측정 분석해줘"처럼 프롬프트로 질의하거나, 팟캐스트 생성 에이전트를 구축할 수 있습니다. 인증 오류 시 `nlm login` 재실행으로 해결하세요.[^3]

Antigravity와 잘 맞는 프로젝트인가요?
<span style="display:none">[^10][^11][^12][^13][^14][^15][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.youtube.com/watch?v=geBad4VaEPI

[^2]: https://www.youtube.com/watch?v=IMFiasVnc0o\&list=PLw3yKt5Xy47EiF4wExBLIJOGprJvvjB5I\&index=2

[^3]: https://www.youtube.com/watch?v=IMFiasVnc0o

[^4]: https://wikidocs.net/329268

[^5]: https://www.youtube.com/watch?v=BpRmVfsB2fk

[^6]: https://www.elancer.co.kr/blog/detail/1046

[^7]: https://juliangoldie.com/notebooklm-with-antigravity-ai-agent-skills/

[^8]: https://tilnote.io/pages/6975cd03078ba21fa0b5ad35

[^9]: https://note.com/masahirokawai/n/n1aef81c144f5

[^10]: https://lilys.ai/ko/notes/openai-agent-builder-20260208/build-chatbot-google-antigravity-notebooklm-mcp-vibe-coding

[^11]: https://lilys.ai/ko/notes/google-antigravity-20260113/notebooklm-google-antigravity-build-anything

[^12]: https://www.reddit.com/r/nocode/comments/1r89roy/bridging_notebooklm_and_antigravity_ide_macos/

[^13]: https://brunch.co.kr/@kap/1699

[^14]: https://www.xda-developers.com/pairing-google-antigravity-and-notebooklm/

[^15]: https://www.youtube.com/watch?v=E7VAaLEg6Zk

