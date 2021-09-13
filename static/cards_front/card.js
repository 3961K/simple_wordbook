Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        id: '',
        word: '',
        answer: '',
        author: '',
        display_status: true,
        is_can_copy: false
    },
    created: function() {
        // URLからカードIDを取得
        this.id = window.location.pathname.split('/')[2];
        // インスタンス作成時に各パラメータを初期化する
        axios.get(
            `/api/v1/cards/${this.id}/`
        )
        .then(response => {
            if (response.status == 200){
                this.word = response.data.word;
                this.answer = response.data.answer;
                this.author = response.data.author_name;
                this.is_can_copy = true;
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
        change_display_status: function() {
            this.display_status = !this.display_status;
        },
        copy: function() {
            // CSRFTokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // 現在表示しているカードのword, answerをパラメータとして設定
            const params = {
                word: this.word,
                answer: this.answer,
                is_hidden: true,
            }
            // 現在表示しているカードのword, answerを利用して新しいカードを取得
            axios.post('/api/v1/cards/', params, {headers: headers})
            .then(response => {
                // コピーに成功した場合はその事を表示する
                if (response.status == 201){
                    window.alert('カードをコピーしました。');
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                if (error.response.status == 403) {
                    window.location.href = '/error/403/';
                }
                else
                {
                    window.alert('カードのコピーに失敗しました。');
                }
            })
        }
    },
})