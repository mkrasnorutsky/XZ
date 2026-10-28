#include <lzma.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
int main(void) {
    const uint8_t input[] = "OneClickPilot liblzma package round-trip: airport and aircraft data.";
    uint8_t compressed[1024], decoded[sizeof(input)];
    size_t compressed_size=0, input_position=0, output_position=0;
    uint64_t memory_limit=UINT64_MAX;
    lzma_ret result=lzma_easy_buffer_encode(6,LZMA_CHECK_CRC64,NULL,input,sizeof(input),compressed,&compressed_size,sizeof(compressed));
    if(result!=LZMA_OK)return 1;
    result=lzma_stream_buffer_decode(&memory_limit,0,NULL,compressed,&input_position,compressed_size,decoded,&output_position,sizeof(decoded));
    if(result!=LZMA_OK || output_position!=sizeof(input) || memcmp(input,decoded,sizeof(input)))return 2;
    if(lzma_version_number()!=LZMA_VERSION)return 3;
    puts("PASS: liblzma encode/decode round-trip and header/library version match");
    return 0;
}
