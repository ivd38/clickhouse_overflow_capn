Clickhouse  heap overflow

```
$ ./clickhouse-client --query "select version()"
22.8.1.1


Processors/Formats/Impl/CapnProtoRowInputFormat.cpp:

j::Array<capnp::word> CapnProtoRowInputFormat::readMessage()
{
    uint32_t segment_count;
    in->readStrict(reinterpret_cast<char*>(&segment_count), sizeof(uint32_t));

    // one for segmentCount and one because segmentCount starts from 0
    const auto prefix_size = (2 + segment_count) * sizeof(uint32_t);
[1]    const auto words_prefix_size = (segment_count + 1) / 2 + 1;
[2]    auto prefix = kj::heapArray<capnp::word>(words_prefix_size);
    auto prefix_chars = prefix.asChars();
    ::memcpy(prefix_chars.begin(), &segment_count, sizeof(uint32_t));

    // read size of each segment
[3]    for (size_t i = 0; i <= segment_count; ++i)
        in->readStrict(prefix_chars.begin() + ((i + 1) * sizeof(uint32_t)), sizeof(uint32_t));

    ...
}

Type of 'words_prefix_size' is unsigned int, see line #1.
If we set 'segment_count' to 0xffffffff, 'words_prefix_size' will be set to 1.
Thus, small buffer will be allocated on line #2.
On loop #3 heap overflow happens.

How to test:
1. copy test.capnp to 'format_schemes' directory

2. generate 1.bin
$ ./t1.py

3. prepare tables
$ ./t1.sh

4. trigger overflow
$ ./t2.sh

Debug session:
$ gdb -q ./clickhouse-server
...
Thread 3 "HTTPHandler" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7fff663ff700 (LWP 22578)]
0x000000000f694fae in DB::ReadBuffer::next (this=0x7fff4bf273c0) at ./src/IO/ReadBuffer.h:64
64	./src/IO/ReadBuffer.h: No such file or directory.
(gdb) bt 4
#0  0x000000000f694fae in DB::ReadBuffer::next (this=0x7fff4bf273c0) at ./src/IO/ReadBuffer.h:64
#1  DB::ConcatReadBuffer::nextImpl (this=0x7fff4bf510e0) at ./src/IO/ConcatReadBuffer.h:66
#2  0x000000000583f539 in DB::ReadBuffer::next (this=0x7fff4bf510e0) at ./src/IO/ReadBuffer.h:64
#3  DB::ReadBuffer::eof (this=0x7fff4bf510e0) at ./src/IO/ReadBuffer.h:98
(More stack frames follow...)
(gdb) x/10i $pc
=> 0xf694fae <DB::ConcatReadBuffer::nextImpl()+78>:	callq  *0x38(%rax)
   0xf694fb1 <DB::ConcatReadBuffer::nextImpl()+81>:	test   %al,%al
   0xf694fb3 <DB::ConcatReadBuffer::nextImpl()+83>:	
    je     0xf694fe6 <DB::ConcatReadBuffer::nextImpl()+134>
   0xf694fb5 <DB::ConcatReadBuffer::nextImpl()+85>:	lea    0x8(%rbx),%rax
   0xf694fb9 <DB::ConcatReadBuffer::nextImpl()+89>:	mov    %rbx,%rcx
   0xf694fbc <DB::ConcatReadBuffer::nextImpl()+92>:	add    $0x18,%rcx
   0xf694fc0 <DB::ConcatReadBuffer::nextImpl()+96>:	mov    (%rcx),%rcx
   0xf694fc3 <DB::ConcatReadBuffer::nextImpl()+99>:	add    0x40(%rbx),%rcx
   0xf694fc7 <DB::ConcatReadBuffer::nextImpl()+103>:	mov    %rcx,(%rax)
   0xf694fca <DB::ConcatReadBuffer::nextImpl()+106>:	movq   $0x0,0x40(%rbx)
(gdb) i r rax
rax            0x1111111111111111  1229782938247303441
```

Issue is fixed already.

