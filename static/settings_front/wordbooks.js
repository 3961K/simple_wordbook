Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        username: '',
        q: '',
        wordbooks_per_page: [],
        wordbooks_display_status: [],
        current_page_num: 0,
        next_page: false,
        previous_page: false,
    },
    created: async function() {
        // ユーザ名を取得する
        this.username = document.getElementById('username').getAttribute('value');
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
                window.alert(error.response.data);
            })
        },
        redirect_wordbook_url: function(wordbook_id) {
            // 単語帳の詳細ページへ遷移する
            window.location.href = `/wordbooks/${wordbook_id}/`;
        },
        get_edit_wordbook_page_url: function(wordbook_id) {
            // 単語帳の編集ページへのリンクを作成
            return `/settings/wordbooks/${wordbook_id}/add-cards/`;
        },
        delete_wordbook: function(wordbook_id, wordbook_index) {
            // 削除するか確認
            const wordbook_name = this.wordbooks_per_page[wordbook_index].wordbook_name;
            if (!window.confirm(`${wordbook_name}を削除しますか?`)) {
                return;
            }
            // csrftokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // 指定した単語帳を削除
            axios.delete(
                `/api/v1/wordbooks/${wordbook_id}/`, {headers: headers}
            )
            .then(response => {
                // カードの削除に成功した事を表示して,ページを再読み込み
                window.alert('カードの削除に成功しました。');
                location.reload();
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('カード情報の取得に失敗しました。');
            })   
        }
    }
})