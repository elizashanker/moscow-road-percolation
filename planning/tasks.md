# Задачи проекта

В каждой задаче есть шаги, место сохранения результата и вклад в статью. Персональные назначения ожидают GitHub-ников.

| ID | Задача | Срок | Результат |
|---|---|---|---|
| T01 | Зафиксировать протокол и границы первой версии | 2026-11-18 → 2026-11-19 | docs/methodology.md; docs/decisions.md |
| T02 | Разобрать Li 2015 и Zeng 2019 | 2026-11-18 → 2026-11-20 | docs/literature-review.md; docs/references.md |
| T03 | Проверить запуск проекта у всей команды | 2026-11-18 → 2026-11-19 | docs/setup-check.md; docs/how-to-work.md; docs/team.md |
| T04 | Проверить административные границы двух районов | 2026-11-19 → 2026-11-20 | data/raw/khamovniki.geojson и data/raw/basmanny.geojson; reports/figures/boundaries_check.png; docs/data-check.md |
| T05 | Сохранить исходные графы дорог и метаданные | 2026-11-20 → 2026-11-21 | data/raw/<район>_directed.graphml; data/processed/<район>.graphml; data/processed/<район>_metadata.json; docs/data-check.md |
| T06 | Описать исходную связность районов | 2026-11-21 → 2026-11-22 | reports/tables/baseline.csv; reports/figures/<район>_baseline.png; docs/baseline-notes.md |
| T07 | Проверить случайные перекрытия | 2026-11-20 → 2026-11-22 | src/road_percolation/simulation.py; tests/test_simulation.py; docs/methodology.md |
| T08 | Реализовать выбор центра и локальные перекрытия | 2026-11-21 → 2026-11-23 | src/road_percolation/simulation.py; tests/test_simulation.py; reports/figures/local_closure_example.png; docs/methodology.md |
| T09 | Проверить метрики на контрольных графах | 2026-11-20 → 2026-11-22 | tests/test_simulation.py; docs/validation.md |
| T10 | Провести пилот на двух районах | 2026-11-23 → 2026-11-24 | reports/tables/pilot_<район>_<сценарий>.csv; docs/pilot.md; configs/experiment.toml |
| T11 | Выполнить основной пакет экспериментов | 2026-11-24 → 2026-11-25 | reports/tables/runs_<район>_<сценарий>.csv; reports/tables/run_manifest.json; scripts/run_experiments.py |
| T12 | Оценить пороги и неопределённость | 2026-11-25 → 2026-11-26 | reports/tables/summary_<район>_<сценарий>.csv; reports/tables/thresholds.csv; reports/figures/connectivity_curves.png; docs/statistics.md |
| T13 | Подготовить карты до и после распада | 2026-11-25 → 2026-11-26 | reports/figures/<район>_<сценарий>_before.png; reports/figures/<район>_<сценарий>_near_threshold.png; reports/figures/<район>_<сценарий>_after.png; paper/figures.md |
| T14 | Сравнить районы и проверить гипотезы | 2026-11-26 → 2026-11-26 | docs/findings.md; reports/tables/comparison.csv |
| T15 | Проверить влияние объездов за границей района | 2026-11-25 → 2026-11-26 | configs/boundary-check.toml; reports/tables/boundary_sensitivity.csv; docs/boundary-sensitivity.md |
| T16 | Воспроизвести пилот другой участницей | 2026-11-26 → 2026-11-27 | docs/reproduction-check.md; README.md |
| T17 | Собрать отчёт и презентацию | 2026-11-26 → 2026-11-27 | reports/presentation/project.pptx; reports/presentation/project.pdf; reports/presentation/speaker-notes.md |
| T18 | Провести общую проверку основной версии | 2026-11-27 → 2026-11-27 | docs/mvp-review.md; paper/manuscript.md; reports/presentation/ |
| T19 | Исправить замечания и проверить итоговый комплект | 2026-11-28 → 2026-11-29 | docs/revision-log.md; paper/manuscript.md; reports/presentation/ |
| T20 | Сравнить дополнительные районы | 2026-11-30 → 2026-12-04 | configs/experiment.toml; reports/tables/; docs/extensions/additional-districts.md |
| T21 | Построить модель метро с пешими подходами | 2026-11-30 → 2026-12-08 | src/road_percolation/multimodal.py; configs/metro.toml; reports/tables/metro_comparison.csv; docs/extensions/metro.md |
| T22 | Проверить доступность данных о пробках и рельефе | 2026-11-30 → 2026-12-04 | docs/extensions/data-feasibility.md; docs/decisions.md |
| T23 | Подготовить финальный комплект к сдаче | 2026-12-14 → 2026-12-16 | reports/final/; docs/submission-check.md |
| T24 | Провести репетицию и защитить проект | 2026-12-15 → 2026-12-17 | reports/presentation/speaker-notes.md; docs/defense-questions.md; docs/defense-notes.md |
| T25 | Подготовить общий файл научной статьи | 2026-11-18 → 2026-11-20 | paper/manuscript.md; paper/README.md; paper/contributions.md |
| T26 | Написать введение и обзор исследований | 2026-11-19 → 2026-11-23 | paper/manuscript.md; paper/references.bib; docs/literature-review.md |
| T27 | Написать раздел о данных и методах | 2026-11-20 → 2026-11-24 | paper/manuscript.md; configs/experiment.toml; docs/methodology.md |
| T28 | Написать результаты и подготовить подписи к рисункам | 2026-11-25 → 2026-11-26 | paper/manuscript.md; paper/figures.md; reports/tables/ |
| T29 | Написать обсуждение, ограничения и выводы | 2026-11-26 → 2026-11-27 | paper/manuscript.md; docs/findings.md |
| T30 | Написать аннотацию и проверить статью целиком | 2026-11-27 → 2026-11-27 | paper/manuscript.md; paper/review-checklist.md; docs/revision-log.md |
