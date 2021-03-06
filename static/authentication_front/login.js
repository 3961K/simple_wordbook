const app = new Vue({
    el: '#app',
    data: {
        username: '',
        password: '',
    },
    methods: {
        clear_data: function() {
            this.username = '';
            this.password = '';
        },
        login: function() {
            // CSRFTokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // 送信するユーザ名・パスワードを取得する
            const params = {
                username: this.username,
                password: this.password,
            }
            // 入力されたユーザ名・パスワードを送信して認証
            axios.post('/api/v1/authentication/login/', params, {headers: headers})
            .then(response => {
                // ログインに成功した場合はリダイレクトさせる
                if (response.status == 200){
                    window.location.href = '/';
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('ログインに失敗しました。');
                this.clear_data();
            })
        }
    }
})