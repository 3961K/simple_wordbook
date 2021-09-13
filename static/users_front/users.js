Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        q: '',
        users_per_page: [],
        current_page_num: 0,
        next_page: false,
        previous_page: false,
    },
    created: function() {
        // インスタンス作成時に各パラメータを初期化する
        this.get_users_per_page(1);
    },
    methods: {
        get_users_per_page: function(page_number, with_q=false){
            // 指定したページ,パラメータを利用してユーザの情報の取得を行う
            let params = {page: page_number};
            if (with_q) {
                params['q'] = this.q;
            }
            axios.get(
                '/api/v1/users/',
                {
                    params: params
                }
            )
            .then(response => {
                if (response.status == 200){
                    this.users_per_page = response.data.results;
                    this.current_page_num = page_number;
                    this.next_page = response.data.next;
                    this.previous_page = response.data.previous;
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('ユーザ情報の取得に失敗しました。');
            })
        },
        get_user_page_url: function(username) {
            return `/users/${username}/`;
        }
    }
})