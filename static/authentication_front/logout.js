const app = new Vue({
    el: '#app',
    created: function() {
        // CSRFTokenを取得
        const csrftoken = $cookies.get('csrftoken');
        const headers = {'X-CSRFToken': csrftoken};

        axios.post('/api/v1/authentication/logout/', {},{headers: headers})
        .then(response => {
            // ログアウトに成功した場合はリダイレクトさせる
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
})
