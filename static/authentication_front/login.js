const app = new Vue({
    el: '#app',
    data: {
        username: '',
        password: '',
    },
    methods: {
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
                    // 成功した事をalertなどで表示する場合はここに記述
                    window.location.href = '/authentication/login/';
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                let error_message = '';
                console.log(error.response.data);
                for (const [key, value] of Object.entries(error.response.data)) {
                    if (key == 'non_field_errors') {
                        error_message += `${value}\n`;
                    } else {
                        error_message += `${key}は${value}\n`;
                    }
                }
                window.alert(error_message);
            })
        }
    }
})