# hack-apac-keyword
This API extracts keywords related to the worries from the text of the worries that the user has submitted.
The extracted keywords are then used in the News API to extract articles related to the worries.
Specifically, keywords related to the user's concerns are prepared in advance in a dictionary, and the dictionary is checked against the morphologically analyzed words from the user's concerns.
The dictionary is then checked against the morphologically analyzed words in the text of the user's concerns, and articles can be extracted by searching for the matching keywords using the NewAPI.
Users can get hints from the related articles and keywords related to their worries, which will be useful in solving their problems.

feature：   Morphological analysis, worries dictionary, articles related to worries extraction

## Reqirement
 - Python：3.9
 - Openshift:
 - NewsAPI
 - DeepL

## API List
| Name                                    | Method       | URI            |
| ----------------------------------------| ------------ | -------------- |
| [Get keyword](docs/keyword.md)          | GET          | /api/keyword   |
| [Get keyword&search](keyword&search.md) | GET          | /api/keysearch |

## OpenShift Deploy Method

Open shift image 
https://access.redhat.com/documentation/ja-jp/openshift_container_platform/4.3/html/cli_tools/openshift-cli-oc
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