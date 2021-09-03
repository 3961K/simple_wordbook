const app = new Vue({
    el: '#app',
    data: {
        username: '',
        email: '',
        password: '',
        password2: '',
    },
    methods: {
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
                let error_message = '';
                console.log(error.response.data);
                for (const [key, value] of Object.entries(error.response.data)) {
                    if (key == 'non_field_errors') {
                        error_message += `${value}\n`;
                    } else {
                        error_message += `${key}: ${value}\n`;
                    }
                }
                window.alert(error_message);
            })
        }
    }
})