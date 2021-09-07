Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        q: '',
        cards_per_page: [],
        cards_display_status: [],
        current_page_num: 0,
        next_page: false,
        previous_page: false,
    },
    created: function() {
        // インスタンス作成時に各パラメータを初期化する
        this.get_cards_per_page(1);
    },
    methods: {
        get_cards_per_page: function(page_number, with_q=false){
            // 指定したページ,パラメータを利用してユーザの情報の取得を行う
            let params = {page: page_number};
            if (with_q) {
                params['q'] = this.q;
            }
            axios.get(
                '/api/v1/cards/',
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