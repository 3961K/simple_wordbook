const app = new Vue({
    el: '#app',
    data: {
        username: '',
        email: '',
        password: '',
        password2: '',
    },
    methods: {
        clear_data: function() {
            this.username = '';
            this.email = '';
            this.password = '';
            this.password2 = '';
        },
        register: function() {
            // CSRFTokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // 送信するユーザ名・メールアドレス・パスワードを取得する
            const params = {
                username: this.username,
                email: this.email,
                password: this.password,
                password2: this.password2,
            }
            // 入力されたユーザ名・メールアドレス・パスワードを送信してユーザ登録を行う
            axios.post('/api/v1/authentication/register/', params, {headers: headers})
            .then(response => {
                // ユーザ登録に成功した場合はリダイレクトさせる
                if (response.status == 201){
                    // 成功した事をalertなどで表示する場合はここに記述
                    window.location.href = '/authentication/login/';
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('ユーザ登録に失敗しました。');
                this.clear_data();
            })
        }
    }
})