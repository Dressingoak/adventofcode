pub fn md5(input: &[u8]) -> u128 {
    const S: [u32; 64] = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, //  0..15
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, // 16..31
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, // 32..47
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, // 48..63
    ];
    const K: [u32; 64] = [
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, //  0.. 3
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, //  4.. 7
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, //  8..11
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, // 12..15
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, // 16..19
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, // 20..23
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, // 24..27
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, // 28..31
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, // 32..35
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, // 36..39
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, // 40..43
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, // 44..47
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, // 48..51
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, // 52..55
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, // 56..59
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391, // 60..63
    ];

    let mut a0: u32 = 0x67452301; // A
    let mut b0: u32 = 0xefcdab89; // B
    let mut c0: u32 = 0x98badcfe; // C
    let mut d0: u32 = 0x10325476; // D

    let mut message = input.to_vec();
    message.push(0x80);
    while message.len() % 64 != 56 {
        message.push(0x00);
    }
    let input_len_bits = (input.len() as u64).wrapping_mul(8).to_le_bytes();
    message.extend(input_len_bits);
    assert_eq!(0, message.len() % 64);
    for chunk in message.chunks(64) {
        let m: [u32; 16] = chunk
            .chunks(4)
            .map(|bytes| {
                bytes
                    .try_into()
                    .expect("64-byte slice should by chunkable into 16 2-byte arrays")
            })
            .map(|bytes: [u8; 4]| u32::from_le_bytes(bytes))
            .collect::<Vec<u32>>()
            .try_into()
            .expect("Expected exactly 16 u32 values");

        let mut a = a0;
        let mut b = b0;
        let mut c = c0;
        let mut d = d0;

        for i in 0..64 {
            let (mut f, g): (u32, usize);
            match i {
                0..16 => {
                    f = (b & c) | (!b & d);
                    g = i;
                }
                16..32 => {
                    f = (d & b) | (!d & c);
                    g = (5 * i + 1) % 16;
                }
                32..48 => {
                    f = b ^ c ^ d;
                    g = (3 * i + 5) % 16;
                }
                48..64 => {
                    f = c ^ (b | !d);
                    g = (7 * i) % 16;
                }
                _ => unreachable!(),
            };
            f = f.wrapping_add(a).wrapping_add(K[i]).wrapping_add(m[g]);
            a = d;
            d = c;
            c = b;
            b = b.wrapping_add(f.rotate_left(S[i]));
        }
        a0 = a0.wrapping_add(a);
        b0 = b0.wrapping_add(b);
        c0 = c0.wrapping_add(c);
        d0 = d0.wrapping_add(d);
    }

    u128::from_be_bytes(
        // from_be_bytes when inputs are listed a0, b0, ...
        [
            a0.to_le_bytes(),
            b0.to_le_bytes(),
            c0.to_le_bytes(),
            d0.to_le_bytes(),
        ]
        .concat()
        .try_into()
        .unwrap(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_md5() {
        // Empty string
        let hash = md5("".as_bytes());
        let repr = format!("{:032x}", hash);
        assert_eq!("d41d8cd98f00b204e9800998ecf8427e", repr);

        // "The quick brown fox jumps over the lazy dog"
        let hash = md5("The quick brown fox jumps over the lazy dog".as_bytes());
        let repr = format!("{:032x}", hash);
        assert_eq!("9e107d9d372bb6826bd81d3542a419d6", repr);
    }
}
