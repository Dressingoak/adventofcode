#pragma once

#include <array>

namespace utils {

    template<unsigned...>struct seq { using type = seq; };
    template<unsigned N, unsigned... Is>
    struct gen_seq_x : gen_seq_x<N - 1, N - 1, Is...> {};
    template<unsigned... Is>
    struct gen_seq_x<0, Is...> : seq<Is...> {};
    template<unsigned N>
    using gen_seq = typename gen_seq_x<N>::type;

    constexpr const unsigned char2uint(const char c)
    {
        return c - '0';
    }

    template<std::size_t N, std::size_t M, unsigned...I1, unsigned...I2>
    constexpr const std::array<unsigned, M> combine_impl(const char(&data)[N + 1], seq<I1...>, seq<I2...>)
    {
        return { { char2uint(data[I1])..., (I2 + N + 1)...} };
    }

    template<std::size_t N, std::size_t M = N>
    constexpr const std::array<unsigned, M> combine(const char(&data)[N + 1])
    {
        return combine_impl<N, M>(data, gen_seq < N > {}, gen_seq < M - N > {});
    }

}
