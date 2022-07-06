package com.example.aoppractice2.repository;

import com.example.aoppractice2.domain.History;

import org.springframework.data.repository.Repository;

public interface HistoryRepository extends Repository<History, Long> {

    void save(History history);

    History findByLoginId(String loginId);
}
