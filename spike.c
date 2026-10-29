#include <stdint.h>

/* S.P.I.K.E Substitution Permutation Iterative Key Encryption */
/* KryptoMagick (Karl Zander utep.shaadm@gmail.com */

struct spike_ctx {
    uint8_t S[256];
    uint8_t ACC;
    uint8_t TMP;
    uint8_t O;
};

void spike_ksa(struct spike_ctx *ctx, uint8_t *key, int key_len, uint8_t *nonce, int nonce_len) {
    int i;
    for (i = 0; i < 256; i++) {
        ctx->S[i] = (uint8_t)i;
    }
    ctx->ACC = 0;
    ctx->TMP = 0;
    ctx->O = 0;

    uint8_t j = 0;
    uint8_t c = 0;
    for (i = 0; i < 256; i++) {
        j = (j + ctx->S[j] + c) & 0xFF;
        uint8_t k = key[i % key_len];
        ctx->TMP = ctx->S[j];
        ctx->S[j] = ctx->S[k];
        ctx->S[k] = ctx->TMP;
        c = (c + 1) & 0xFF;
    }
    for (i = 0; i < 256; i++) {
        j = (j + ctx->S[j] + c) & 0xFF;
        uint8_t k = nonce[i % nonce_len];
        ctx->TMP = ctx->S[j];
        ctx->S[j] = ctx->S[k];
        ctx->S[k] = ctx->TMP;
        c = (c + 1) & 0xFF;
    }
}

static inline void spike_update(struct spike_ctx *ctx) {
    ctx->ACC = (ctx->ACC + ctx->S[ctx->S[0]]) & 0xFF;
    ctx->O = ctx->S[ctx->S[ctx->S[ctx->ACC]]];
    ctx->TMP = ctx->S[0];
    ctx->S[0] = ctx->S[ctx->ACC];
    ctx->S[ctx->ACC] = ctx->TMP;
}

uint8_t spike_crypt(struct spike_ctx *ctx, uint8_t in) {
    spike_update(ctx);
    return in ^ ctx->O;
}
