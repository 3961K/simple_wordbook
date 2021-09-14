Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        username: '',
        q: '',
        cards_per_page: [],
        cards_display_status: [],
        current_page_num: 0,
        next_page: false,
        previous_page: false,
    },
    created: function() {
        // ユーザ名を取得
        this.username = document.getElementById('username').getAttribute('value');
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
                `/api/v1/users/${this.username}/cards/`,
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
                window.alert('カード情報の取得に失敗しました。');
            })
        },
        get_card_page_url: function(card_id) {
            // カードの詳細ページへのリンクを作成
            return `/cards/${card_id}/`;
        },
        get_edit_card_page_url: function(card_id) {
            // カードの編集ページへのリンクを作成
            return `/settings/cards/${card_id}/`;
        },
        delete_card: function(card_id, card_index) {
            // 削除するか確認
            let partial_card_word = this.cards_per_page[card_index].word.substring(0, 10);
            if (this.cards_per_page[card_index].word.substring(0, 10).length > 10) {
                partial_card_word += '...';
            }
            window.confirm(`${partial_card_word}を削除しますか?`);
            // csrftokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // 指定したカードを削除
            axios.delete(
                `/api/v1/cards/${card_id}/`, {headers: headers}
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