# 📡 Speedtest Discord Bot

Discordに定期的にインターネット速度をEmbed形式で投稿するBotです。Ookla公式CLIを使用し、Ping・Download・Upload・国旗・前回との差分などを視覚的に表示します。

---

## 🧩 主な機能

- 📶 1時間ごとにSpeedtest結果を自動投稿（起動直後にも即時投稿）
- 🕐 投稿タイミングは毎時00分に固定（例: 10:00, 11:00）
- 🎮 DiscordプレゼンスにPingを5分おきに表示
- 🌐 国コードから国旗を表示（不明時は🌐）
- 🟢🟡🔴 Ping品質を自動判定
- ⬆️⬇️ 前回の速度との増減を表示（差分）
- 📦 Docker Swarmで運用、Secrets対応
- 🔁 GHCRにGitHub Actionsで自動ビルド＆公開

---

## 🚀 セットアップ手順

### 1. GitHubへPushして自動ビルド

```bash
git clone https://github.com/<your-username>/speedtest-discord-bot.git
cd speedtest-discord-bot
# 修正後、以下を実行
git add .
git commit -m "Initial commit"
git push origin main
```

※ `GHCR` へ `docker/build-push-action` により自動ビルド＆公開されます。

---

### 2. Discord Botの作成・設定

1. Discord Developer PortalでBotを作成
2. Bot Tokenを取得
3. サーバーにBotを招待し、**「メッセージ送信・プレゼンス更新」** 権限を付与
4. 投稿先のチャンネルIDを控える

---

### 3. Docker Swarmでの起動

#### ⛓️ Secrets作成

```bash
echo "YOUR_DISCORD_BOT_TOKEN" | docker secret create DISCORD_TOKEN -
echo "YOUR_CHANNEL_ID" | docker secret create DISCORD_CHANNEL_ID -
```

#### 🧱 起動（ビルド済みイメージを使用）

```bash
docker stack deploy -c docker-compose.yml speedtestbot
```

#### 🔁 更新

```bash
docker service update --force speedtestbot_speedtest-bot
```

---

## 📁 ディレクトリ構成

```
speedtest-discord-bot/
├── bot/
│   ├── main.py             # Discord Bot本体
│   └── speedtest.py        # Speedtest実行ロジック（国旗・差分含む）
├── Dockerfile              # 軽量Python + タイムゾーン JST対応
├── requirements.txt        # 必要なPythonライブラリ（discord.py 等）
├── docker-compose.yml      # Swarm用サービス定義
└── .github/workflows/      # GitHub ActionsによるGHCRビルド設定
```

---

## 🔧 カスタマイズ例

| 項目 | 方法 |
|------|------|
| 投稿間隔を変えたい | `main.py` の `speedtest_scheduler` を修正 |
| サーバーを変更したい | `speedtest.py` の `--server-id` を変更 |
| プレゼンスをOFFにしたい | `ping_status_loop` タスクを無効化 |

---

## 📜 ライセンス

MIT License

---

## 💬 サポート

質問や要望があれば [Issues](https://github.com/<your-repo>/issues) へどうぞ！
