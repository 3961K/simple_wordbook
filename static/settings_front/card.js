Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        username: '',
        id: '',
        word: '',
        answer: '',
        author: '',
        is_hidden: false,
    },
    created: function() {
        // ユーザ名を取得する
        this.username = document.getElementById('username').getAttribute('value');
        // URLからIDを取得する
        this.id = window.location.pathname.split('/')[3];
        // インスタンス作成時に各パラメータを初期化する
        axios.get(
            `/api/v1/cards/${this.id}/`
        )
        .then(response => {
            if (response.status == 200){
                this.author = response.data.author_name;
                if (this.username != this.author) {
                    // 作者でないのに編集しようとした場合は403へリダイレクト
                    window.location.href = '/error/403/';
                }
    
                this.word = response.data.word;
                this.answer = response.data.answer;
                this.is_hidden = response.data.is_hidden;
            }
        })
        .catch(error => {
            // ステータスコードが2XXでなかった場合はalertでリダイレクトまたはエラー内容を表示
            switch (error.response.status) {
                case 403:
                    window.location.href = '/error/403/';
                    break;
                case 404:
                    window.location.href = '/error/404/';
                    break;
                default:
                    window.alert('カード情報が取得できませんでした。');
                    break;
            }
        })
    },
    methods: {
        update_card: function() {
            // CSRFTokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // 送信するword, answer, is_hiddenをparamsとしてまとめる
            const params = {
                'word': this.word,
                'answer': this.answer,
                'is_hidden': this.is_hidden
            };
            console.log(params);
            // word, answer, is_hiddenを送信してカードを作成
            axios.patch(
                `/api/v1/cards/${this.id}/`, params, {headers: headers}
            )
            .then(response => {
                if (response.status == 200){
                    // カードの更新に成功した事を表示する
                    window.alert('カードの更新に成功しました。');
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('カードの更新に失敗しました。');
            })
        }
    },
})