Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        word: '',
        answer: '',
        is_hidden: false,
    },
    methods: {
        create_card: function() {
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
            axios.post(
                '/api/v1/cards/', params, {headers: headers}
            )
            .then(response => {
                if (response.status == 201){
                    // カードの作成に成功した事を表示し,フォームに入力された値をクリアする
                    this.word = '';
                    this.answer = '';
                    this.is_hidden = false;
                    window.alert('カードの作成に成功しました');
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert(error.response.data);
            })
        }
    },
})