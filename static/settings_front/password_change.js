Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        username: '',
        old_password: '',
        password: '',
        password2: '',
    },
    created: function() {
        // ユーザ名を取得
        this.username = document.getElementById('username').getAttribute('value');
    },
    methods: {
        clear_data: function() {
            // パスワードに関するパラメータを初期化する
            this.old_password = '';
            this.password = '';
            this.password2 = '';
        },
        update_password: function() {
            // CSRFトークンを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // 元のパスワードと新しいパスワードを送信するパラメータとして取得
            const params = {
                'old_password': this.old_password,
                'password': this.password,
                'password2': this.password2
            };
            console.log(params);
            // パスワード更新を試みる
            axios.patch(
                `/api/v1/users/${this.username}/change-password/`, params, {headers: headers}
            )
            .then(response => {
                // パスワードの更新に成功した旨を表示
                if (response.status == 200){
                    window.alert('パスワードの更新に成功しました。');
                }
                this.clear_data();
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('パスワードの更新に失敗しました。');
                this.clear_data();
            })
        }
    },
})