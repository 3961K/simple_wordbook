# simple wordbook 説明

## 概要

- simple wordbookはRESTfulなWeb APIの基礎・基本的な内容の学習としてDjango REST Framework(以下DRF)を用いて作成した単語カードの作成機能や単語カードの集合である単語帳の作成機能など持つ単語帳に関するアプリケーションです。
- Web APIのエンドポイントを利用する簡易的なVue.jsを用いたWebのフロントエンドを実装しております。
- simple wordbookはデプロイしておりませんので、ソースコードと下記の機能の説明を参照して、アプリケーションの内容をご理解して頂けると幸いです。

## ER図

![ER](https://user-images.githubusercontent.com/80889322/137634806-b66ac771-28e4-424c-9916-29caf637b01f.png)

## 利用している主要なライブラリ

### バックエンド

- Django
- djangorestframework
- django-filter
- PyMySQL
- Pillow

### フロントエンド

- Vue.js
- axios
- vue-cookies

## Cardモデルについて

### 概要

- Cardモデルは他のユーザに対して公開・非公開を指定する事が可能な、単語カードを意味するモデルです。

### 重要なフィールド

- word
  - 単語カードの単語を格納するCharFieldです。(単語カードの表のイメージです。)

- answer
  - 単語カードの単語の答えを格納するCharFieldです。(単語カードの裏のイメージです。)

- is_hidden
  - 単語カードがauthorで指定する作者以外の他のユーザからアクセスする事が出来るか否かを格納するBooleanFieldです。
  - 以下の説明において 公開状態 とはis_hiddenがFalseに設定されており全てのユーザからアクセスする事が可能である状態を指し、 非公開状態 とはis_hiddenがTrueに設定されており自身以外がアクセスする事が可能でない状態を指します。

- author
  - 単語カードを作成したUserモデルの識別子を格納するForeignKeyです。

- wordbooks
  - 単語カードが属するWordbookモデルの識別子を格納するManyToManyFieldです。

## Wordbookモデルについて

### 概要

- Wordbookモデルは他のユーザに対して公開・非公開を指定する事が可能な、単語カードの集合である単語帳を意味するモデルです。

### 重要なフィールド

- is_hidden
  - 単語帳がauthorで指定する作者以外の他のユーザからアクセスする事が出来るか否かを格納するBooleanFieldです。
  - Cardモデルと同様に以下の説明において 公開状態 とはis_hiddenがFalseに設定されており全てのユーザからアクセスする事が可能である状態を指し、 非公開状態 とはis_hiddenがTrueに設定されており自身以外がアクセスする事が可能でない状態を指します。

- author
  - 単語帳を作成したUserモデルの識別子を格納するForeignKeyです。

## 認証に関する機能

### 登録

#### Web APIエンドポイント

- /api/v1/authentication/register/ に対して、ユーザ名・メールアドレス・パスワード・確認用のパスワードを入力してPOSTメソッドでHTTPリクエストを送信する事でユーザ登録をする事が可能です。

- (例) testuserの登録する時のリクエストとレスポンス

![register](https://user-images.githubusercontent.com/80889322/137635728-2879466f-878f-458d-b10c-b7c0854abdd6.png)
![register_result](https://user-images.githubusercontent.com/80889322/137634264-b56b5861-6d91-425b-a3c8-b5bf39b201fd.png)

#### Web フロントエンド

- /authentication/register/ にアクセスして、必要な情報を入力して ユーザ登録 を選択する事でユーザ登録する事が可能です。
- ユーザ登録 が選択された時に/api/v1/authentication/register/に対して必要な情報をPOSTメソッドでHTTPリクエストを送信し、ユーザ登録を行っております。

![login](https://user-images.githubusercontent.com/80889322/137634542-53c52ea6-1ece-4fa7-92f9-e717553c85ec.png)

### ログイン

#### Web APIエンドポイント

- /api/v1/authentication/login/ に対して、ユーザ名・パスワードを入力してPOSTメソッドでHTTPリクエストを送信する事でログインする事が可能です。

- (例)　testuserとしてログインする時のリクエストとレスポンス

![login](https://user-images.githubusercontent.com/80889322/137635566-0e4ebfe6-e14a-464c-a324-7a139f6e45ce.png)
![login_result](https://user-images.githubusercontent.com/80889322/137634257-6df06da0-c3e1-4cae-a5bd-518a2a5dd77f.png)

#### Web フロントエンド

- /authentication/login/ にアクセスして、ユーザ名とパスワードを入力して ログイン を選択する事でログインする事が可能です。
- ログイン が選択された時に/api/v1/authentication/login/に対してユーザ名・パスワードをPOSTメソッドでHTTPリクエストを送信し、ログインを行っております。

![login](https://user-images.githubusercontent.com/80889322/137635474-41c2dd04-b235-4c79-9478-2785420e120b.png)

### ログアウト

#### Web APIエンドポイント

- /api/v1/authentication/logout/ に対して、ログインしている状態でPOSTメソッドでHTTPリクエストを送信する事でログアウトする事が可能です。

- (例) ログアウト時のリクエストとレスポンス

![logout](https://user-images.githubusercontent.com/80889322/137634260-94d8725d-def5-42a9-9b75-e676ca2e5896.png)
![logout_result](https://user-images.githubusercontent.com/80889322/137634261-c357b19b-a44c-4005-bb9d-2c454d7ef467.png)

#### Web フロントエンド

- ログインしている状態でページ上部の logout を選択する事でログアウトする事が可能です。
- logout が選択された時に/api/v1/authentication/logout/に対してPOSTメソッドでHTTPリクエストを送信し、ログアウトを行っております。

![logout](https://user-images.githubusercontent.com/80889322/137634549-716fb9e2-64b8-420f-859a-5da09dff9392.png)

## カード(card)に関する機能

### カード検索　

#### Web API

- /api/v1/cards/に対して、GETメソッドでHTTPリクエストを送信する事でページングされた公開状態であるカード一覧を取得する事が可能です。
- qパラメータを利用する事で、指定した文字列をWordに含むカードのみに絞り込み検索をする事が可能です。
- ログインしている場合は自身が作成した非公開状態のカードも一覧に含まれます。

- (例)　/cards/へのリクエストとレスポンス

![cards](https://user-images.githubusercontent.com/80889322/137634288-9cbc79be-cdba-4786-a1fa-eb38354c44ac.png)

- (例) /cards/?q=landへのリクエストとレスポンス

![cards_q](https://user-images.githubusercontent.com/80889322/137634294-b6f857db-fb8a-4ce7-9a44-7bcd0b839d2c.png)

#### Web フロントエンド

- /cards/に対してGETメソッドでHTTPリクエストを送信する事でページングされたカード一覧を以下の様に取得する事が可能です。
- /cards/にアクセスした時または異なるページへアクセスした時に、/api/v1/cards/に対して非同期でGETメソッドでHTTPリクエストを送信する事でページングされたカード一覧を取得しております。

![cards](https://user-images.githubusercontent.com/80889322/137634569-2e7c2b6c-1ce5-4045-be2e-0c4a54a758c3.gif)

### カード作成

#### Web API

- /api/v1/cards/に対して、ログインしている状態でword・answer・is_hiddenをPOSTメソッドでHTTPリクエストを送信する事で新規カードを作成する事が可能です。
- is_hiddenをFalseにしてカードを作成するとそのカードは非公開状態となり、仮に他のユーザが単語帳の作成時・単語帳へのカード追加時に非公開状態のカードのIDを追加しようとしても追加する事が不可能となります。(非公開状態カードの作者としてログインしている場合は単語帳に追加する事が可能です。)

- (例) /api/v1/cards/に対する新規カード作成時のリクエストとレスポンス

![create_new_card](https://user-images.githubusercontent.com/80889322/137634295-aff1cfe7-918f-49a8-9984-a5a248b3b13c.png)
![create_new_card_result](https://user-images.githubusercontent.com/80889322/137634297-31dc1965-6e1a-4f8c-8738-48156f5f989e.png)

#### Web フロントエンド

- ログインしている状態で/cards/new-card/においてword・answer・is_hiddenに任意の値を指定した状態で 作成 を選択する事で、以下の様にカードを作成する事が可能です。
- 作成 が選択された時に、/api/v1/cards/に対して非同期でPOSTメソッドでカードの情報をHTTPリクエストで送信する事でカードの作成を行っております。

![create_card](https://user-images.githubusercontent.com/80889322/137634579-77d1d5ce-9c84-483e-bfef-bb4458d81385.gif)

### カード情報取得

#### Web API

- /api/v1/cards/\<uuid:id\>/に対して、GETメソッドでHTTPリクエストを送信する事で指定したカードが公開状態である場合にword・answer・カードの作者名を取得する事が可能です。
- ログインしている場合は自身が作成した非公開状態のカードであれば、同様にカードの情報を取得する事が可能です。

- (例) /api/v1/cards/\<uuid:id\>/に対するカード情報取得時のリクエストとレスポンス

![card](https://user-images.githubusercontent.com/80889322/137634300-a212eba1-0a51-4818-ab3c-0dfdf1a937f6.png)

#### Web フロントエンド

- /cards/\<uuid:id\>/にアクセスする事で、指定したカードのWordとAnswerの情報を取得する事が可能です。
  - /cards/\<uuid:id\>/には以下の様にカードのWordまたはAnswerに格納されている文字列を選択する事でアクセスする事が可能です。
- /cards/\<uuid:id\>/にアクセスした時に、/api/v1/cards/\<uuid:id\>/に対してGETメソッドでHTTPリクエストを送信する事でカードの情報を取得しております。

![detail_card](https://user-images.githubusercontent.com/80889322/137634581-1b3d6dee-97b2-41c5-bbb4-4c5d33cccda2.gif)

### カード更新

#### Web API

- /api/v1/cards/\<uuid:id\>/に対して、対象のカードの作者としてログインしている場合にPATCHメソッドで新しいword・answer・is_hiddenをHTTPリクエストで送信する事で指定したカードの情報を更新する事が可能です。
  - 対象のカードの作者としてログインしないでPATCHメソッドでカードの更新を試みようとした場合は、カードの更新は行われず403が返されます。

#### Web フロントエンド

- ログインしている状態で/settings/cards/\<uuid:id\>/にアクセスし、対象のカードのword・answer・is_hiddenの新しい値を設定し 更新 を選択する事で、カードの更新を行う事が可能です。
  - 更新 が選択された時に、/api/v1/cards/\<uuid:id\>/に対して非同期でPATCHメソッドで新しいカードの情報をHTTPリクエストで送信する事でカード情報の更新を行っております。
  - /settings/にアクセスして カード管理 を選択する事でカードの一覧ページ(/settings/cards/)にアクセスし、そこから任意のカードの 編集ボタン を選択する事でカードの編集ページにアクセスする事が可能です。
  - 自分が作成していないカードのUUIDを指定した場合は、403ページへリダイレクトされます。

### カード削除

#### Web API

- /api/v1/cards/\<uuid:id\>/に対して、対象のカードの作者としてログインしている場合にDELETEメソッドでHTTPリクエストを送信する事で指定したカードを削除する事が可能です。
  - 対象のカードの作者としてログインしないでDELETEメソッドでカードの削除を試みようとした場合は、カードの削除は行われず403が返されます。

#### Web フロントエンド

- ログインしている状態で/settings/cards/にアクセスし、任意のカードの 削除ボタン を選択する事でカードの削除を行う事が可能です。
  - 削除ボタン が選択された時に/api/v1/cards/\<uuid:id\>/に対してDELETEメソッドでHTTPリクエストを送信する事でカードの削除を行っております。

![delete_card](https://user-images.githubusercontent.com/80889322/137634580-2dc0eb06-816c-4ccd-9e29-61a6b91329fc.gif)

## 単語帳(wordbook)に関する機能

### 単語帳検索

#### Web API

- /api/v1/wordbooks/に対して、GETメソッドでHTTPリクエストを送信する事でページングされた公開状態である単語帳一覧を取得する事が可能です。
- qパラメータを利用する事で、指定した文字列を単語帳名に含む単語帳のみに絞り込み検索をする事が可能です。
- ログインしている場合は自身が作成した非公開状態の単語帳も一覧に含まれます。

- (例)　/api/v1/wordbooks/に対するリクエストとレスポンス

![wordbooks](https://user-images.githubusercontent.com/80889322/137634474-37071373-b9d4-4dac-8525-1847aad36b09.png)

- (例) /api/v1/wordbooks/?q=虫に対するリクエストとレスポンス

![wordbooks_q](https://user-images.githubusercontent.com/80889322/137634475-d476d700-ffb8-482f-aad5-5997bc849aea.png)

#### Web フロントエンド

- /wordbooks/に対してGETメソッドでHTTPリクエストを送信する事でページングされた単語帳一覧を以下の様に取得する事が可能です。
  - /wordboks/にアクセスした時に、/api/v1/wordbooks/に対して非同期でGETメソッドでHTTPリクエストを送信する事でページングされた単語帳一覧の取得を行っております。

![wordbooks](https://user-images.githubusercontent.com/80889322/137634648-8882590c-688a-437b-bad9-afd09db41034.gif)

### 単語帳作成

#### Web API

- /api/v1/wordbooks/に対して、ログインしている状態でwordbook_name・is_hiddenをPOSTメソッドでHTTPリクエストを送信する事で単語帳を作成する事が可能です。

- (例) /api/v1/wordbooks/に対して単語帳を作成する時のリクエストとレスポンス

![create_new_wordbook](https://user-images.githubusercontent.com/80889322/137634465-79490ffa-5940-4520-a8ef-09b881e997b1.png)
![create_new_wordbook_result](https://user-images.githubusercontent.com/80889322/137634467-fa33838f-485d-4964-94a1-42747a527036.png)

#### Web フロントエンド

- ログインしている状態で/wordbooks/new-card/にアクセスし、単語帳に含みたいカードの選択と単語帳名・公開属性の設定を行った上で 単語帳作成 を選択する事で、指定したカードを含む単語帳を作成する事が可能です。
  - 単語帳作成時には以下の2つ工程を行っております。
  - (工程1) /api/v1/wordbooks/に対して非同期でPOSTメソッドで単語帳名・公開属性をHTTPリクエストを送信して単語帳の作成を行う。
  - (工程2) 工程1の結果が成功した場合に/api/v1/wordbooks/\<uuid:id\>/に対して指定カードのIDをadd_cardsに指定した状態で、非同期でPATCHメソッドでHTTPリクエストを送信する事で指定したカードを含む単語帳を作成しております。

![create_wordbook](https://user-images.githubusercontent.com/80889322/137634643-38ed4881-7d03-438e-9768-6fef4060e31d.gif)

### 単語帳の情報を取得する

#### Web API

- /api/v1/wordbooks/\<uuid:id\>/に対して、GETリクエストを送信する事で対象の単語帳が公開状態であった場合に単語帳名・作成日・作者名などを取得する事が可能です。
- 対象の単語帳の作者としてログインしている場合は非公開状態の単語帳の情報を取得する事も可能です。

- (例) /api/v1/wordbooks/\<uuid:id\>/に対する単語帳を作成する時のリクエストとレスポンス

![wordbook](https://user-images.githubusercontent.com/80889322/137634471-fcc0344c-aa69-4eed-b093-2749bb888c92.png)

### 単語帳に含まれるカードを取得する

#### Web API

- /api/v1/wordbooks/\<uuid:id\>/cards/に対して、GETメソッドでHTTPリクエストを送信する事で対象の単語帳が公開状態であった場合に、ページングされた対象の単語帳に含まれている公開状態のカードの一覧を取得する事が可能です。
- 対象の単語帳の作者としてログインしている場合は非公開状態の単語帳のカードも含めて取得する事が可能です。

- (例) /api/v1/wordbooks/\<uuid:id\>/cards/に対する単語帳に含まれているカードの一覧を取得する時のリクエストとレスポンス

![wordbook_cards](https://user-images.githubusercontent.com/80889322/137634472-2ffbcaea-334e-4275-9cc7-d60a659886f1.png)

#### Web フロントエンド

- /wordbooks/\<uuid:id\>/にアクセスする事で、ページングされた対象の単語帳に含まれているカードの一覧を以下の様に取得する事が可能です。
  - /wordbooks/\<uuid:id\>/にアクセスした時または異なるページへアクセスした時に、/api/v1/wordbooks/\<uuid:id\>/と/api/v1/wordbooks/\<uuid:id\>/cards/にGETメソッドでHTTPリクエストを送信し、対象の単語帳の情報とページングされた対象の単語帳に含まれるカードの一覧を取得しております。

![detail_wordbook](https://user-images.githubusercontent.com/80889322/137634647-e82fdaf5-9db9-478a-9dc9-9d438ce6ccf0.gif)

### 単語帳を更新する

#### Web API

- /api/v1/wordbooks/\<uuid:id\>/cards/に対して、その単語帳の作者としてログインしている場合に、PATCHメソッドで単語帳名・公開属性・単語帳に追加するカードのUUIDの配列・単語帳から削除したカードのUUIDの配列を指定してHTTPリクエストを送信する事で、指定した単語帳を更新する事が可能です。
- 単語帳が公開状態である場合に非公開カードを追加した場合は、自身以外のユーザからその単語帳のカード一覧にアクセスされた時に非公開カードを除いたカードのみ返すため、非公開カードの内容は公開されず自身が単語帳にアクセスした場合にのみ非公開カードが含まれた状態のカード一覧を取得する事が可能です。

- (例) /api/v1/wordbooks/\<uuid:id\>/cards/に対して単語帳にカードを追加する時のリクエストとレスポンス

![add_cards_to_wordbook](https://user-images.githubusercontent.com/80889322/137634454-e557811d-6b7a-45c3-88e0-c1c1c7f9691c.png)
![add_cards_to_wordbook_response](https://user-images.githubusercontent.com/80889322/137634459-ca49dcd3-a5af-439b-a8d0-80e7483fd227.png)

- (例) /api/v1/wordbooks/\<uuid:id\>/cards/に対して単語帳からカードを削除する時のリクエストとレスポンス

![delete_cards_from_wordbook](https://user-images.githubusercontent.com/80889322/137634468-e1991fd6-b0cf-4072-9ea4-86e8b33bf65d.png)
![delete_cards_from_wordbook_response](https://user-images.githubusercontent.com/80889322/137634469-c83ac8ab-0189-4cd2-af10-528cfa6476fd.png)

#### Web フロントエンド (カードの追加)

- ログインしている状態で/settings/wordbooks/\<uuid:id\>/add-cards/にアクセスし、単語帳に追加したいカードをカード一覧から選択して 選択したカードを追加 を選択する事で、単語帳にカードを追加する事が可能です。
  - 選択したカードを追加 を選択した時にadd_cardsに追加するカードのIDを格納した状態で/api/v1/wordbooks/\<uuid:id\>/cards/に対して非同期でPATCHメソッドでHTTPリクエストを送信する事で、単語帳にカードを追加しております。
  - カード追加ページへはログインした状態で/settings/の 単語帳管理 を選択して単語帳一覧ページにアクセスし、そこから任意の単語帳の 削除ボタン を選択する事でアクセスする事が可能です。
  - 自分が作成していないカードのUUIDを指定した場合は、カード追加ページ・カード削除ページどちらにおいても403ページへリダイレクトされます。

![add_cards_to_wordbook](https://user-images.githubusercontent.com/80889322/137634639-534ebe79-f409-41f9-90b6-658b77edaf12.gif)

#### Web フロントエンド (カードの削除)

- ログインしている状態で/settings/wordbooks/\<uuid:id\>/delete-cards/にアクセスし、単語帳に含まれているカード一覧から任意のカードの 削除ボタン を選択する事で、単語帳からカードを削除する事が可能です。
  - 削除ボタン を選択した時にdel_cardsに削除したいカードのIDを格納した状態で/api/v1/wordbooks/\<uuid:id\>/cards/に対して非同期でPATCHメソッドでHTTPリクエストを送信する事で、単語帳からカードの削除を行っております。
  - 単語帳からカードを削除したい場合は カードの削除 をカード追加ページから選択する事でカード削除ページへアクセスする事が可能です。

![delete_cards_from_wordbooks](https://user-images.githubusercontent.com/80889322/137634645-f3d7b155-5912-4844-830c-80a7411d9220.gif)

### 単語帳を削除する

#### Web API

- /api/v1/wordbooks/\<uuid:id\>/に対して、その単語帳の作者としてログインしている場合にDELETEメソッドでHTTPリクエストを送信する事で、指定した単語帳を削除する事が可能です。

#### Web フロントエンド

- ログインしている状態で/settings/wordbooks/にアクセスし、そこから任意の単語帳の 削除ボタン を選択する事で指定した単語帳を削除する事が可能です。
  - 削除ボタン が選択された時に、/api/v1/wordbooks/\<uuid:id\>/に対してDELETEメソッドでHTTPリクエストを送信する事で単語帳の削除を行っております。

![delete_wordbook](https://user-images.githubusercontent.com/80889322/137634646-ff79448c-97b3-4866-a6be-547fad395f91.gif)

## ユーザに関する機能

### ユーザ検索

#### Web APIエンドポイント

- /api/v1/users/に対して、GETメソッドでHTTPリクエストを送信する事でページングされたユーザ一覧を取得する事が可能です。
- qパラメータを利用する事で、指定した文字列をユーザ名に含むユーザのみに絞り込み検索をする事が可能です。

- (例) /api/v1/users/に対して、ユーザ一覧を取得する時のリクエストとレスポンス

![users](https://user-images.githubusercontent.com/80889322/137634359-b06bbf10-383d-4e35-bc09-131e683f3679.png)

- (例) /api/v1/users/?q=5に対して、ユーザ一覧を取得する時のリクエストとレスポンス

![users_q](https://user-images.githubusercontent.com/80889322/137634363-5aeffd04-f632-4ac1-8bad-82ed96ec6396.png)

#### Web フロントエンド

- /users/に対してGETメソッドでHTTPリクエストを送信する事でページングされたユーザ一覧を以下の様に取得する事が可能です。
  - /users/にアクセスした時または異なるページへアクセスした時に、/api/v1/users/に対して非同期でGETメソッドでHTTPリクエストを送信する事でページングされたユーザ一覧を取得しております。

![users](https://user-images.githubusercontent.com/80889322/137634616-69214b27-131a-4987-8752-93e33a29304d.gif)

### 指定したユーザ情報の取得

#### Web APIエンドポイント

- /api/v1/users/\<str:username\>/に対して、GETメソッドでHTTPリクエストを送信する事で指定したユーザのユーザ名とアイコンを取得する事が可能です。

- (例) /api/v1/users/\<str:username\>/に対して、ユーザ情報を取得する時のリクエストとレスポンス

![user](https://user-images.githubusercontent.com/80889322/137634369-bcb209d6-8f6a-428d-9508-efa88d52d9a0.png)

### 指定したユーザが作成したカード一覧の取得

#### Web APIエンドポイント

- /api/v1/users/\<str:username\>/cards/に対して、GETメソッドでHTTPリクエストを送信する事でページングされた指定したユーザが作成した公開状態のカードの一覧を取得する事が可能です。
- 指定したユーザとしてログインしている場合は非公開状態のカードも含めて取得する事が可能です。
- qパラメータを利用する事で、指定した文字列をWordに含むカードのみに絞り込み検索をする事が可能です。

- (例) /api/v1/users/\<str:username\>/cards/に対して、カード一覧を取得する時のリクエストとレスポンス

![user_cards](https://user-images.githubusercontent.com/80889322/137634370-72ab6d5a-d9f1-4d3d-97a4-5e6300032316.png)

- (例) /api/v1/users/\<str:username\>/cards/?q=appleに対して、カード一覧を取得する時のリクエストとレスポンス

![user_cards_q](https://user-images.githubusercontent.com/80889322/137634371-22f5af47-6bc5-440d-9441-b220206ac46f.png)

#### Web フロントエンド

- /users/\<str:username\>/に対してGETメソッドでHTTPリクエストを送信する事でページングされた指定したユーザが作成したカード一覧を以下の様に取得する事が可能です。
  - /users/\<str:username\>/にアクセスした時または異なるページへアクセスした時に、/api/v1/users/\<str:username\>/cards/に対して非同期でGETメソッドでHTTPリクエストを送信する事でページングされた指定したユーザが作成したカード一覧を取得しております。

![user_cards](https://user-images.githubusercontent.com/80889322/137634612-fb184aaf-9830-45ff-9dd5-aa1c9da7940a.gif)

### 指定したユーザが作成した単語帳一覧の取得

#### Web APIエンドポイント

- /api/v1/users/\<str:username\>/wordbooks/に対して、GETメソッドでHTTPリクエストを送信する事でページングされた指定したユーザが作成した公開状態である単語帳の一覧を取得する事が可能です。
- 指定したユーザとしてログインしている場合は非公開状態である単語帳も含めて取得する事が可能です。
- qパラメータを利用する事で、指定した文字列を単語帳名に含む単語帳のみに絞り込み検索をする事が可能です。

- (例) /api/v1/users/\<str:username\>/wordbooks/に対して、単語帳一覧を取得する時のリクエストとレスポンス

![user_wordbooks](https://user-images.githubusercontent.com/80889322/137634373-14022fe2-7555-4af4-aa7f-11d8ee1d2508.png)

- (例) /api/v1/users/\<str:username\>/wordbooks/?q=2に対して、単語帳一覧を取得する時のリクエストとレスポンス

![user_wordbooks_q](https://user-images.githubusercontent.com/80889322/137634374-7d1ec951-bc66-4dc3-833d-265e5994801a.png)

#### Web フロントエンド

- /users/\<str:username\>/wordbooks/に対してGETメソッドでHTTPリクエストを送信する事でページングされた指定したユーザが作成した単語帳一覧を以下の様に取得する事が可能です。
  - /users/\<str:username\>/wordbooks/にアクセスした時または異なるページへアクセスした時に、/api/v1/users/\<str:username\>/wordbooks/に対して非同期でGETメソッドでHTTPリクエストを送信する事でページングされた指定したユーザが作成した単語帳一覧を取得しております。

![user_wordbooks](https://user-images.githubusercontent.com/80889322/137634614-f3498ec7-886d-4104-84d9-1404b190d42e.gif)

### ユーザのプロフィールを更新する

#### Web フロントエンド

- ログインしている状態で/settings/user-info/にアクセスし、新しいユーザ名・メールアドレス・アイコンを指定して ユーザ情報更新 を選択する事でユーザのプロフィールを更新する事が可能です。
  - ユーザ情報更新を選択した時に、/api/v1/users/\<str:username\>/に対して非同期でPATCHメソッドで更新する情報をHTTPリクエストで送信する事で、プロフィールの更新を行っております。

![change_user_profile](https://user-images.githubusercontent.com/80889322/137634609-efeaf6fa-e753-4d2f-af45-e17ee7d4d995.png)

### ユーザのパスワードを変更する

#### Web APIエンドポイント

- /api/v1/users/\<str:username\>/change-password/に対して、指定したユーザとしてログインしている場合にPATCHメソッドで現在のパスワード・新しいパスワード・新しいパスワード(確認用)をHTTPリクエストで送信する事でパスワードを変更する事が可能です。

- (例) /api/v1/users/\<str:username\>/change-password/に対して、パスワードを更新する時のリクエストとレスポンス

![change_password](https://user-images.githubusercontent.com/80889322/137635796-b42cfc14-7b98-4bef-a246-735d2bf87eea.png)
![change_password_result](https://user-images.githubusercontent.com/80889322/137634327-af0c17a7-d6cf-4c98-8cee-9ef7e703bec9.png)

#### Web フロントエンド

- ログインしている状態で/settings/password-change/にアクセスし、現在のパスワード・新しいパスワード・新しいパスワード(確認用)を指定して パスワード更新 を選択する事でユーザのパスワードを更新する事が可能です。
  - ユーザ情報更新を選択した時に、/api/v1/users/\<str:username\>/change-password/に対して非同期でPATCHメソッドで更新する情報をHTTPリクエストで送信する事で、プロフィールの更新を行っております。

![change_user_password](https://user-images.githubusercontent.com/80889322/137634608-ef23683d-d2a2-45bf-8367-df72effe4b0f.png)

### ユーザを削除する 

#### Web APIエンドポイント

- /api/v1/users/\<str:username\>/に対して、指定したユーザとしてログインしている場合にDELETEリクエストを送信する事で指定したユーザを削除する事が可能です。

#### Web フロントエンド

- ログインしている状態で/settings/delete-user/にアクセスし、削除　を選択する事でユーザアカウントの削除を行う事が可能です。
  - 削除 を選択した時に、/api/v1/users/\<str:username\>/change-password/に対して非同期でDELETEメソッドで更新する情報をHTTPリクエストで送信する事で、ユーザアカウントの削除を行っております。

![delete_user](https://user-images.githubusercontent.com/80889322/137634611-85e76416-19b1-4d65-9ac7-6c7f2fcab58d.png)
