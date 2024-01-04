import os
import glob
import pygit2

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv(), override=True)  # read local .env file

token = os.getenv("GITHUB_ACCESS_TOKEN") or "GITHUB_ACCESS_TOKEN"

projects = [
    "https://github.com/aerius-labs/zk-snap",
    "https://github.com/rpanic/vale-ui",
    "https://github.com/pico-labs/coinflip-executor-contract",
    "https://github.com/alysiahuggins/proof-of-ownership-zkapp",
    "https://github.com/sausage-dog/minanite",
    "https://github.com/iammadab/dark-chess",
    "https://github.com/gretzke/zkApp-data-types",
    "https://github.com/Sr-santi/mina-ui",
    "https://github.com/Trivo25/offchain-voting-poc",
    "https://github.com/gordonfreemanfree/snarkyjs-ml",
    "https://github.com/chainwayxyz/mCash",
    "https://github.com/mitschabaude/snarkyjs-sudoku",
    "https://github.com/yunus433/snarkyjs-math",
    "https://github.com/RaidasGrisk/zkapp-ui",
    "https://github.com/jackryanservia/wordle",
    "https://github.com/anandcsingh/rankproof",
    "https://github.com/mina-arena/Contracts",
    "https://github.com/zkHumans/zkHumans",
    "https://github.com/zkHumans/zk-kv",
    "https://github.com/racampos/cpone",
    "https://github.com/SutuLabs/MinaCTF",
    "https://github.com/WalletZkApp/zk-keyless-wallet-contracts",
    "https://github.com/AdMetaNetwork/admeta-mina-chort-1",
    "https://github.com/devarend/binance-oracle",
    "https://github.com/snarky-bio/biosnarks",
    "https://github.com/zk0ath/usdm",
    "https://github.com/garethtdavies/zkAppPool",
    "https://github.com/palladians/herald",
    "https://github.com/anandcsingh/keito",
    "https://github.com/Identicon-Dao/socialcap",
    "https://github.com/anandcsingh/whisper-key",
    "https://github.com/boidushya/ZeroID",
    "https://github.com/microbecode/zk-agecheck",
    "https://github.com/iam-robi/zkapp-monorepo",
    "https://github.com/kaupangdx/kaupangdx",
    "https://github.com/Lumina-DEX/lumina-interface-new",
    "https://github.com/frisitano/mina-swap",
    "https://github.com/BerzanXYZ/xane",
    "https://github.com/Muhammad-Altabba/snarkyjs-tender",
    "https://github.com/wotomas/BlindMansBluff",
    "https://github.com/petemccarthy/bullscows",
    "https://github.com/vimukthi-git/CheckerSnapp",
    "https://github.com/cannsky/ForgottenEmpires",
    "https://github.com/iam-robi/zkapp-guesser-race",
    "https://github.com/0xtito/hot-n-cold",
    "https://github.com/MinaPoker/contract",
    "https://github.com/sCrypt-Inc/mina-wordle",
    "https://github.com/teddyjfpender/motomon",
    "https://github.com/mirceanis/prove-my-turn",
    "https://github.com/Raunaque97/RepeatingLifeZK",
    "https://github.com/frisitano/snapp-hangman",
    "https://github.com/rudrakpatra/zkchess",
    "https://github.com/teddyjfpender/anon-ballots",
    "https://github.com/aerius-labs/zk-voting-poc-fe",
    "https://github.com/madztheo/zk-voting-web-app",
    "https://github.com/45930/mina-navi-voting-demo",
    "https://github.com/45930/Voting-Playground-o1js",
    "https://github.com/yunus433/zkvote",
    "https://github.com/TokeniZK/tokenizk-finance",
    "https://github.com/iluxonchik/zkLocus",
    "https://github.com/only4sim/Snarky-ML",
    "https://github.com/devarend/binance-zkapp",
    "https://github.com/45930/canvas-zk-contracts",
    "https://github.com/Esayf/Examina",
    "https://github.com/microbecode/mina_devdao_hackathon",
    "https://github.com/kriss1897/zk-invoices",
    "https://github.com/marekyggdrasil/mac",
    "https://github.com/0xStruct/moolah",
    "https://github.com/openmina/mina-load-generator",
    "https://github.com/plus3-labs/shadow",
    "https://github.com/Kirol54/minaBootcamp",
    "https://github.com/45930/zk-todo",
    "https://github.com/BadmWe/WebBadminton",
    "https://github.com/enderNakamoto/zkMile-contracts",
    "https://github.com/kyok01/zkBookReview",
    "https://github.com/dfstio/minanft-lib",
    "https://github.com/comdex/nft-zkapp",
    "https://github.com/LastCeri/MogartNetwork",
    "https://github.com/chrlyz/wrdhom_contracts",
    "https://github.com/suenchunhui/mina-privacy-coin",
    "https://github.com/AlexFedotovqq/TradeCoin",
    "https://github.com/mlabs-haskell/MinAuth",
    "https://github.com/JoE11-y/MVS",
    "https://github.com/kriss1897/zk-social-recovery",
    "https://github.com/julio4/zap",
]

os.makedirs("projects", exist_ok=True)


def clone_github_project(repo_link):
    try:
        parts = repo_link.strip("/").split("/")
        owner, repo = parts[-2], parts[-1]

        repoClone = pygit2.clone_repository(repo_link, f"./projects/{repo}")
    except Exception as e:
        print(f"An unexpected error occurred while cloning {repo_link}: {e}")

for repo_link in projects:
    clone_github_project(repo_link)
