package com.example.aoppractice2.common;

import com.example.aoppractice2.domain.History;
import com.example.aoppractice2.repository.HistoryRepository;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class LoggingAspect {

    @Autowired
    private HistoryRepository historyRepository;

    @Pointcut(value = "execution(* com.example.aoppractice2.service.UserService.login(..))")
    public void login() {
    }

    @AfterReturning("login()")
    public void afterLoginSuccess(JoinPoint joinPoint) {
        String loginId = String.valueOf(joinPoint.getArgs()[0]);
        historyRepository.save(History.create(true, loginId, "SUCCESS"));
        System.out.println("SUCCESS!!");
    }

    @AfterThrowing("login()")
    public void afterLoginFail(JoinPoint joinPoint) {
        String loginId = String.valueOf(joinPoint.getArgs()[0]);
        historyRepository.save(History.create(false, loginId, "FAIL"));
        System.out.println("FAIL!!");
    }
}
