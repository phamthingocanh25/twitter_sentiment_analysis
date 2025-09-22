import math
import numpy as np
from .utils import process_tweet

# Các đại từ ngôi thứ nhất và thứ hai
FIRST_SECOND_PRONOUNS = {
    "i", "me", "my", "mine", "we", "us", "our", "ours",
    "you", "your", "yours", "u", "ya"
}

def extract_features(tweet, freqs):
    """
    Trích xuất 6 đặc trưng từ một tweet.
    Input:
        tweet: chuỗi string thô của tweet
        freqs: từ điển ánh xạ (từ, nhãn) -> tần suất
    Output:
        x: vector đặc trưng (1, 7) bao gồm [bias, x1..x6]
    """
    # Kiểm tra dấu '!' trên tweet thô
    has_exclaim = "!" in (tweet or "")

    # Xử lý token (stem, loại bỏ stopwords...)
    word_l = process_tweet(tweet)
    wc = len(word_l)

    # Khởi tạo vector [bias + 6 features]
    x = np.zeros((1, 7))
    x[0, 0] = 1.0  # bias

    # x1, x2: tổng tần suất từ tích cực và tiêu cực
    pos_sum, neg_sum = 0.0, 0.0
    for w in word_l:
        if (w, 1.0) in freqs:
            pos_sum += freqs[(w, 1.0)]
        if (w, 0.0) in freqs:
            neg_sum += freqs[(w, 0.0)]

    # x3: có từ "no"?
    has_no = 1.0 if "no" in word_l else 0.0

    # x4: đếm đại từ ngôi 1 & 2
    pron_count = sum(1 for w in word_l if w in FIRST_SECOND_PRONOUNS)

    # x5: có dấu '!' trong tweet thô?
    exclaim = 1.0 if has_exclaim else 0.0

    # x6: ln(word_count)
    ln_wc = math.log(max(1, wc))

    # Gán vào vector
    x[0, 1] = pos_sum
    x[0, 2] = neg_sum
    x[0, 3] = has_no
    x[0, 4] = pron_count
    x[0, 5] = exclaim
    x[0, 6] = ln_wc

    assert x.shape == (1, 7)
    return x
