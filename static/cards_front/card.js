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
            // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
            this.word = 'カード情報が取得できませんでした';
            this.answer = 'カード情報が取得できませんでした';
            this.author = '不明';
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
                let error_message = '';

                if (error.response.status == 403) {
                    error_message = '認証が行われている必要があります';
                }
                else
                {
                    for (const [key, value] of Object.entries(error.response.data)) {
                        if (key == 'non_field_errors') {
                            error_message += `${value}\n`;
                        } else {
                            error_message += `${key}は${value}\n`;
                        }
                    }    
                }
                window.alert(error_message);
            })
        }
    },
})