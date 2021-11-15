# hack-apac-keyword

バックエンド(キーワード抽出API)

アーキテクチャ：
このAPIはユーザーが起票したお悩み文章から悩みに関連したキーワードを抽出し、
抽出したキーワードをNewsAPIに用いて悩みに関連した記事を抽出します。
具体的には辞書に悩みに関するキーワードを事前に用意しユーザーが起票したお悩み文章から形態素解析した単語と辞書で照合し、
照合一致したキーワードをNewAPIで検索かけることで記事を抽出することができてます。
利用者はその関連記事と悩みに関連するキーワードからヒントをもらい、悩みの解決として役に立つでしょう。

特徴：形態素解析、悩み辞書、悩みに関連する記事抽出
## Getting Started

### Setting
1. Docker Imageをダウンロードする
2. Docker FileをOpenshiftに配置する
3. GithubのソースコードをOpenshiftに配置する
4. 起動する

## Reqirement
・Python：3.9
・Image：
・Openshift:
・Docker Image：
    alpine：https://hub.docker.com/_/alpine

・News API
・Deep L

## API List

| Name                                    | Method          | URI            |
| ----------------------------------------| --------------- | -------------- |
| [Get keyword](keyword.md)               | GET             | /api/keyword   |
| [Get keyword&search](keyword&search.md) | POST            | /api/keysearch |


## Example
### OpenShift Deploy Method

`
oc registry login  # 内部レジストリのURLメモっとく($REGISTRY_URLで使う)
oc whoami -t  # パスワードメモっとく
docker login $REGISTRY_URL -u $(oc whoami)  # パスワード求められるから入れる
#cdでdockerfileのあるディレクトリに移動する 
docker login
docker image build -t $IMAGENAME1:VERSION .
docker tag $IMAGENAME1 $DOCKERUSER/$IMAGENAME2
docker push $REGISTRY_URL/IMAGENAME2
oc get is
oc new-app IS-IMAGE #isの中から対象のイメージを指定
oc get is -w

`