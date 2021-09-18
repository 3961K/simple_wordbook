Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        q: '',
        wordbooks_per_page: [],
        wordbooks_display_status: [],
        current_page_num: 0,
        next_page: false,
        previous_page: false,
    },
    created: function() {
        // カードを取得する
        this.get_wordbooks_per_page(1);
    },
    methods: {
        get_wordbooks_per_page: function(page_number, with_q=false) {
            // そのユーザが作成した単語帳の一覧を取得する
            let params = {page: page_number};
            if (with_q) {
                params['q'] = this.q;
            }
            axios.get(
                `/api/v1/wordbooks/`,
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
                window.alert('単語帳の取得に失敗しました。');
            })
        },
        redirect_wordbook_url: function(wordbook_id) {
            window.location.href = `/wordbooks/${wordbook_id}/`;
        }
    }
})