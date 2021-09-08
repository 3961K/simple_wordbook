Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        wordbook_id: '',
        wordbook_name: '',
        wordbook_author_name: '',
        q: '',
        cards_per_page: [],
        cards_display_status: [],
        current_page_num: 0,
        next_page: false,
        previous_page: false,
    },
    created: async function() {
        // 単語帳IDをブラウザに表示されているURLから取得する
        this.wordbook_id = window.location.pathname.split('/')[2];
        // 単語帳の情報を取得する
        this.get_wordbook_information();
        // 単語帳に含まれているカードを取得する
        this.get_cards_per_page(1);
    },
    methods: {
        get_wordbook_information: function() {  
            // 単語帳名・単語帳の作者名を取得する
            axios.get(
                `/api/v1/wordbooks/${this.wordbook_id}/`
            )
            .then(response => {
                if (response.status == 200){
                    this.wordbook_name = response.data.wordbook_name;
                    this.wordbook_author_name = response.data.author_name;
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert(error.response.data);
            })
        },
        get_cards_per_page: function(page_number, is_with_q=false) {
            // そのユーザが作成したカードの一覧を取得する
            let params = {page: page_number};
            if (is_with_q) {
                params['q'] = this.q;
            }
            axios.get(
                `/api/v1/wordbooks/${this.wordbook_id}/cards/`,
                {
                    params: params
                }
            )
            .then(response => {
                if (response.status == 200){
                    this.cards_per_page = response.data.results;
                    this.cards_display_status = Array(this.cards_per_page.length);
                    this.cards_display_status.fill(true);
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
        get_card_page_url: function(card_id) {
            return `/cards/${card_id}/`;
        }
    },
    computed: {
        card_display_status: function() {
            // 指定したカードの表示状態を返す
            return function(index) {
                return this.cards_display_status[index];
            }
        },
        card_content: function() {
            // 指定したカードの表示状態に基づいてwordまたはanswerを返す
            return function(index) {
                this.cards_display_status.splice(index, 1, !this.cards_display_status[index]);
            }
        }
    }
})