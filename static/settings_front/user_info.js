Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        username: '',
        email: '',
        icon_url: '',
    },
    created: function() {
        // ユーザ名を取得
        this.username = document.getElementById('username-form').getAttribute('value');
        // 現在のメールアドレス・アイコン情報を取得
        axios.get(
            `/api/v1/users/${this.username}/`
        )
        .then(response => {
            if (response.status == 200){
                this.email = response.data.email;
                this.icon_url = response.data.icon;
            }
        })
        .catch(error => {
            // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
        })
    },
    methods: {
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
            console.log(icon);
            if (icon) {
                params.append('icon', icon.files[0]);
            }

            console.log(params);

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
                window.alert(error.response.data);
            })
        }
    },
})