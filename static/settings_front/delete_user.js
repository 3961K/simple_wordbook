Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        username: '',
    },
    created: function() {
        this.username = document.getElementById('username').getAttribute('value');
    },
    methods: {
        delete_user: function() {
            // csrftokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // ユーザ削除を行うDELETEメソッドでHTTPリクエストを送信する
            axios.delete(
                `/api/v1/users/${this.username}/`, {headers: headers}
            )
            .then(response => {
                if (response.status == 204) {
                    // ユーザ削除に成功した事を通知した後に/へリダイレクトさせる
                    window.alert('ユーザの削除に成功しました。');
                    window.location.href = '/';
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('ユーザの削除に失敗しました。');
            })
        }
    }
})