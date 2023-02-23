package com.example.hackingspringboot.reactive;

import com.example.hackingspringboot.reactive.ch05.HttpTraceWrapper;
import com.example.hackingspringboot.reactive.ch05.HttpTraceWrapperRepository;
import com.example.hackingspringboot.reactive.ch05.SpringDataHttpTraceRepository;
import java.net.URI;
import java.util.Collections;
import java.util.Map;
import org.bson.Document;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.actuate.trace.http.HttpTrace;
import org.springframework.boot.actuate.trace.http.HttpTraceRepository;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.convert.converter.Converter;
import org.springframework.data.mongodb.core.convert.MappingMongoConverter;
import org.springframework.data.mongodb.core.convert.MongoCustomConversions;
import org.springframework.data.mongodb.core.convert.NoOpDbRefResolver;
import org.springframework.data.mongodb.core.mapping.MongoMappingContext;
import org.thymeleaf.TemplateEngine;
import reactor.blockhound.BlockHound;

@SpringBootApplication
public class HackingSpringBootCh2ReactiveApplication {

    public static void main(String[] args) {
        BlockHound.builder()
            .allowBlockingCallsInside(
                TemplateEngine.class.getCanonicalName(), "process"
            )
            .install();

        SpringApplication.run(HackingSpringBootCh2ReactiveApplication.class, args);
    }

//    @Bean
//    HttpTraceRepository traceRepository() {
//        return new InMemoryHttpTraceRepository();
//    }

    @Bean
    HttpTraceRepository springDataTraceRepository(HttpTraceWrapperRepository repository) {
        return new SpringDataHttpTraceRepository(repository);
    }

    static Converter<Document, HttpTraceWrapper> CONVERTER = //
        new Converter<Document, HttpTraceWrapper>() { //
            @Override
            public HttpTraceWrapper convert(Document document) {
                Document httpTrace = document.get("httpTrace", Document.class);
                Document request = httpTrace.get("request", Document.class);
                Document response = httpTrace.get("response", Document.class);

                return new HttpTraceWrapper(new HttpTrace( //
                    new HttpTrace.Request( //
                        request.getString("method"), //
                        URI.create(request.getString("uri")), //
                        request.get("headers", Map.class), //
                        null),
                    new HttpTrace.Response( //
                        response.getInteger("status"), //
                        response.get("headers", Map.class)),
                    httpTrace.getDate("timestamp").toInstant(), //
                    null, //
                    null, //
                    httpTrace.getLong("timeTaken")));
            }
        };

    @Bean
    public MappingMongoConverter mappingMongoConverter(MongoMappingContext context) {

        MappingMongoConverter mappingConverter = //
            new MappingMongoConverter(NoOpDbRefResolver.INSTANCE, context); // <1>

        mappingConverter.setCustomConversions( // <2>
            new MongoCustomConversions(Collections.singletonList(CONVERTER))); // <3>

        return mappingConverter;
    }
}
