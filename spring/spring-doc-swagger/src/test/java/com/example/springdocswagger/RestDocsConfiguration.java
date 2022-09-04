package com.example.springdocswagger;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.restdocs.mockmvc.MockMvcRestDocumentation;
import org.springframework.restdocs.mockmvc.RestDocumentationResultHandler;
import org.springframework.restdocs.operation.preprocess.Preprocessors;
import org.springframework.restdocs.snippet.Attributes;

@TestConfiguration
public class RestDocsConfiguration {

    @Bean
    public RestDocumentationResultHandler write() {
        return MockMvcRestDocumentation
                .document(
                "{class-name}/{method-name}", // 테스트 코드에서 andDo(document("xxx"))를 반복적으로 넣는 부분 개선
                Preprocessors.preprocessRequest(Preprocessors.prettyPrint()), // build/generated-snippets에 만들어진 파일을 html로 만들 때, json이 한 줄로 출력되던 내용을 pretty 하게 찍어줌.
                Preprocessors.preprocessResponse(Preprocessors.prettyPrint())
        );
    }

    public static final Attributes.Attribute field(
            final String key,
            final String value) {
        return new Attributes.Attribute(key, value);
    }
}
