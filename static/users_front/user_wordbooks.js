Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        username: '',
        icon: '',
        q: '',
        wordbooks_per_page: [],
        wordbooks_display_status: [],
        current_page_num: 0,
        next_page: false,
        previous_page: false,
    },
    created: async function() {
        // ユーザ名をブラウザに表示されているURLから取得する
        const username_in_url = window.location.pathname.split('/')[2];
        await axios.get(
            `/api/v1/users/${username_in_url}/`,
        )
        .then(response => {
            // ユーザ名とアイコンを取得
            if (response.status == 200){
                this.username = response.data.username;
                this.icon = response.data.icon;
            }
        })
        .catch(error => {
            // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
            window.alert('単語帳情報の取得に失敗しました。');
        });
        // カードを取得する
        this.get_wordbooks_per_page(1);
    },
    methods: {
        get_wordbooks_per_page: function(page_number, with_q=false) {
            // そのユーザが作成したカードの一覧を取得する
            let params = {page: page_number};
            if (with_q) {
                params['q'] = this.q;
            }
            axios.get(
                `/api/v1/users/${this.username}/wordbooks/`,
                {
                    params: params
                }
            )
            .then(response => {
                if (response.status == 200){
                    this.wordbooks_per_page = response.data.results;
                    this.wordbooks_display_status = Array(this.wordbooks_per_page.length);
                    this.wordbooks_display_status.fill(true);
                    this.current_page_num = page_number;
                    this.next_page = response.data.next;
                    this.previous_page = response.data.previous;
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('単語帳情報の取得に失敗しました。');
            })
        },
        redirect_wordbook_url: function(wordbook_id) {
            window.location.href = `/wordbooks/${wordbook_id}/`;
        }
    },
    computed: {
        cards_url: function() {
            // ユーザのカード一覧ページのURLを構築する
            return `/users/${this.username}/cards/`;
        },
        wordbooks_url: function() {
            // ユーザの単語帳一覧ページのURLを構築する
            return `/users/${this.username}/wordbooks/`;
        },
        wordbook_display_status: function() {
            // 指定したカードの表示状態を返す
            return function(index) {
                return this.wordbooks_display_status[index];
            }
        },
        wordbook_content: function() {
            // 指定したカードの表示状態に基づいてwordまたはanswerを返す
            return function(index) {
                this.wordbooks_display_status.splice(index, 1, !this.wordbooks_display_status[index]);
            }
        }
    }
})