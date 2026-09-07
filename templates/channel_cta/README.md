# Channel common CTA

`channel_common_cta` は、Episode 003 v3で人間承認されたチャンネル共通のエンドカード構成を、エピソード固有素材から切り離した設定プロファイルです。

- 実行設定: `config/channel_cta.json`
- 標準ロゴ: `local/channel/icon.png`
- 生成器: `scripts/create_channel_cta.py`
- 既定表示: 10秒、static、新しいナレーションなし

新しいEpisodeでは、`episode.json` の `postroll.cta_profile` を `channel_common_cta` とし、`postroll.asset` を `work/channel_cta.png` にします。build前に次を実行するか、builderが同じ設定を使って生成したPNGを指定します。

```powershell
python scripts/create_channel_cta.py --output episodes/NNN_slug/work/channel_cta.png
```

テーマ固有の前Episode CTAを無条件に流用しません。ロゴ、文言、配置を変更する場合は、チャンネル設定と人間レビューを更新します。
