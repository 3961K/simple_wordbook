Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        username: '',
        current_username: '',
        email: '',
        current_email: '',
        icon_url: '',
        current_icon_url: '',
    },
    created: function() {
        // ユーザ名を取得
        this.current_username = document.getElementById('username-form').getAttribute('value')
        this.username = this.current_username;
        // 現在のメールアドレス・アイコン情報を取得
        axios.get(
            `/api/v1/users/${this.username}/`
        )
        .then(response => {
            if (response.status == 200){
                this.current_email = response.data.email;
                this.email = this.current_email;
                this.current_icon_url = response.data.icon;
                this.icon_url = this.current_icon_url;
            }
        })
        .catch(error => {
            // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
        })
    },
    methods: {
        clear_data: function() {
            // パラメータを初期化する
            this.username = this.current_username;
            this.email = this.current_email;
            this.icon_url = this.current_icon_url;
        },
        update_icon: function() {
            const icon_file = this.$refs.icon.files[0];
            this.icon_url = URL.createObjectURL(icon_file);
        },
        update_user_info: function() {
            // CSRFTokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // ユーザ名・メールアドレスを取得
            let params = new FormData();
            params.append('username', this.username);
            params.append('email', this.email);
            // アイコン画像が指定されていない場合はiconを送信しない
            const icon = document.getElementById('new-icon');
            if (icon.files[0]) {
                params.append('icon', icon.files[0]);
            }

            axios.patch(
                `/api/v1/users/${this.username}/`, params, {headers: headers}
            )
            .then(response => {
                // ユーザ情報の更新に成功した旨を表示
                if (response.status == 200){
                    window.alert('ユーザ情報の更新に成功しました。');
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('ユーザ情報の更新に失敗しました。');
                this.clear_data();
            })
        }
    },
})